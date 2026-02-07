import numpy as np
from typing import Tuple, Optional, Dict

class RobotArmIK:
    def __init__(self):
        """Initialize robot arm with segment lengths in mm"""
        self.h_base = 96.1      # Base/shoulder height
        self.L1 = 90.6          # Shoulder to elbow
        self.L2 = 90.6          # Elbow to wrist
        self.L3 = 144.57        # Wrist to grabber
        
        # Servo calibration parameters
        # You'll need to measure and set these for your specific robot
        self.servo_config = {
            'joint1': {'offset': 0.0, 'direction': 1},    # Base rotation
            'joint2': {'offset': 90.0, 'direction': 1},   # Shoulder
            'joint3': {'offset': 0.0, 'direction': -1},   # Elbow
            'joint4': {'offset': 90.0, 'direction': 1}    # Wrist
        }
        
    def set_servo_calibration(self, joint_name: str, offset: float, direction: int):
        """
        Set calibration parameters for a specific joint.
        
        Args:
            joint_name: 'joint1', 'joint2', 'joint3', or 'joint4'
            offset: Angle offset in degrees (what servo angle gives 0° in world space)
            direction: 1 for same direction, -1 for reversed
            
        Example:
            # If servo at 90° corresponds to world angle 0°, and directions match:
            arm.set_servo_calibration('joint2', offset=90.0, direction=1)
            
            # If servo at 180° corresponds to world angle 0°, and reversed:
            arm.set_servo_calibration('joint3', offset=180.0, direction=-1)
        """
        if joint_name in self.servo_config:
            self.servo_config[joint_name]['offset'] = offset
            self.servo_config[joint_name]['direction'] = direction
        else:
            raise ValueError(f"Unknown joint: {joint_name}")
    
    def world_to_servo_angle(self, world_angle: float, joint_name: str) -> float:
        """
        Convert world-space angle to servo command angle.
        
        Args:
            world_angle: Angle in degrees from IK calculation
            joint_name: Which joint ('joint1', 'joint2', etc.)
            
        Returns:
            Servo command angle in degrees
        """
        config = self.servo_config[joint_name]
        servo_angle = config['offset'] + (config['direction'] * world_angle)
        return servo_angle
    
    def servo_to_world_angle(self, servo_angle: float, joint_name: str) -> float:
        """
        Convert servo command angle to world-space angle.
        
        Args:
            servo_angle: Current servo angle in degrees
            joint_name: Which joint ('joint1', 'joint2', etc.)
            
        Returns:
            World-space angle in degrees
        """
        config = self.servo_config[joint_name]
        world_angle = (servo_angle - config['offset']) / config['direction']
        return world_angle
        
    def inverse_kinematics(self, 
                          x: float, 
                          y: float, 
                          z: float, 
                          grabber_angle_deg: float = -90.0,
                          elbow_up: bool = True,
                          return_servo_angles: bool = True) -> Optional[Dict]:
        """
        Calculate inverse kinematics for 4-DOF arm.
        
        Args:
            x: Target x position (mm)
            y: Target y position (mm)
            z: Target z position (mm)
            grabber_angle_deg: Desired angle of grabber relative to horizontal (degrees)
            elbow_up: If True, use elbow-up configuration
            return_servo_angles: If True, return servo command angles; if False, return world angles
            
        Returns:
            Dictionary with 'world_angles' and 'servo_angles', or None if unreachable
        """
        
        # Convert grabber angle to radians
        grabber_angle = np.deg2rad(grabber_angle_deg)
        
        # Step 1: Calculate base rotation (theta1)
        theta1 = np.arctan2(y, x)
        
        # Step 2: Calculate horizontal reach distance
        r_target = np.sqrt(x**2 + y**2)
        
        # Step 3: Calculate wrist position
        r_wrist = r_target - self.L3 * np.cos(grabber_angle)
        z_wrist = z - self.L3 * np.sin(grabber_angle)
        
        # Step 4: Solve 2-link IK for shoulder and elbow
        z_from_shoulder = z_wrist - self.h_base
        d = np.sqrt(r_wrist**2 + z_from_shoulder**2)
        
        # Check if target is reachable
        if d > (self.L1 + self.L2) or d < abs(self.L1 - self.L2):
            print(f"Target unreachable: distance {d:.2f}mm, max reach {self.L1 + self.L2:.2f}mm")
            return None
        
        # Calculate elbow angle
        cos_theta3 = (d**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        cos_theta3 = np.clip(cos_theta3, -1.0, 1.0)
        
        if elbow_up:
            theta3 = np.arccos(cos_theta3)
        else:
            theta3 = -np.arccos(cos_theta3)
        
        # Calculate shoulder angle
        alpha = np.arctan2(z_from_shoulder, r_wrist)
        beta = np.arctan2(self.L2 * np.sin(theta3), self.L1 + self.L2 * np.cos(theta3))
        theta2 = alpha - beta
        
        # Step 5: Calculate wrist angle
        theta4 = grabber_angle - theta2 - theta3
        
        # Convert to degrees
        world_angles = {
            'joint1': np.rad2deg(theta1),
            'joint2': np.rad2deg(theta2),
            'joint3': np.rad2deg(theta3),
            'joint4': np.rad2deg(theta4)
        }
        
        # Convert to servo angles
        servo_angles = {
            joint: self.world_to_servo_angle(angle, joint)
            for joint, angle in world_angles.items()
        }
        
        return {
            'world_angles': world_angles,
            'servo_angles': servo_angles
        }
    
    def forward_kinematics(self, angles: Dict, angle_type: str = 'world') -> Tuple[float, float, float]:
        """
        Calculate end effector position from joint angles.
        
        Args:
            angles: Dictionary with joint angles ('joint1', 'joint2', etc.)
            angle_type: 'world' or 'servo' - specifies the type of input angles
            
        Returns:
            Tuple of (x, y, z) position of grabber tip in mm
        """
        # Convert servo angles to world angles if needed
        if angle_type == 'servo':
            world_angles = {
                joint: self.servo_to_world_angle(angle, joint)
                for joint, angle in angles.items()
            }
        else:
            world_angles = angles
        
        # Convert to radians
        theta1 = np.deg2rad(world_angles['joint1'])
        theta2 = np.deg2rad(world_angles['joint2'])
        theta3 = np.deg2rad(world_angles['joint3'])
        theta4 = np.deg2rad(world_angles['joint4'])
        
        # Calculate in vertical plane
        z_shoulder = self.h_base
        r_shoulder = 0
        
        r_elbow = r_shoulder + self.L1 * np.cos(theta2)
        z_elbow = z_shoulder + self.L1 * np.sin(theta2)
        
        r_wrist = r_elbow + self.L2 * np.cos(theta2 + theta3)
        z_wrist = z_elbow + self.L2 * np.sin(theta2 + theta3)
        
        grabber_angle = theta2 + theta3 + theta4
        r_grabber = r_wrist + self.L3 * np.cos(grabber_angle)
        z_grabber = z_wrist + self.L3 * np.sin(grabber_angle)
        
        # Convert to cartesian
        x = r_grabber * np.cos(theta1)
        y = r_grabber * np.sin(theta1)
        z = z_grabber
        
        return (x, y, z)
    
    def calibrate_joint(self, joint_name: str):
        """
        Interactive calibration helper for a specific joint.
        Prints instructions for determining offset and direction.
        """
        print(f"\n=== Calibrating {joint_name} ===")
        print("\nStep 1: Find the zero offset")
        print("  - Move the arm so this joint is at its 'zero' position in world space")
        print("  - For base (joint1): pointing forward (x-axis)")
        print("  - For shoulder/elbow/wrist: horizontal (0° elevation)")
        print("  - Read the servo angle from your controller")
        print("  - This servo angle is your OFFSET")
        print("\nStep 2: Determine direction")
        print("  - Increase the servo angle by 10-20 degrees")
        print("  - Does the joint rotate in the expected direction?")
        print("    YES → direction = 1")
        print("    NO  → direction = -1")
        print("\nEnter calibration values:")
        
        try:
            offset = float(input(f"  Offset for {joint_name} (degrees): "))
            direction = int(input(f"  Direction for {joint_name} (1 or -1): "))
            self.set_servo_calibration(joint_name, offset, direction)
            print(f"✓ {joint_name} calibrated: offset={offset}°, direction={direction}")
        except ValueError:
            print("Invalid input. Calibration cancelled.")


# Example usage
if __name__ == "__main__":
    arm = RobotArmIK()
    
    # Example calibration (you need to measure these for your robot)
    print("Setting up servo calibration...")
    print("These are EXAMPLE values - you must calibrate your own robot!\n")
    
    # Example: If your servos are mounted such that:
    # - Joint 1 (base): 90° servo = 0° world (pointing forward)
    # - Joint 2 (shoulder): 90° servo = 0° world (horizontal), same direction
    # - Joint 3 (elbow): 180° servo = 0° world (straight), reversed direction
    # - Joint 4 (wrist): 90° servo = 0° world (horizontal), same direction
    
    arm.set_servo_calibration('joint1', offset=90.0, direction=1)
    arm.set_servo_calibration('joint2', offset=90.0, direction=1)
    arm.set_servo_calibration('joint3', offset=180.0, direction=-1)
    arm.set_servo_calibration('joint4', offset=90.0, direction=1)
    
    # Target position
    target_x = 127.0
    target_y = 0.0
    target_z = 10.0
    
    print(f"Target position: ({target_x}, {target_y}, {target_z})")
    
    # Calculate IK
    result = arm.inverse_kinematics(target_x, target_y, target_z, 
                                    grabber_angle_deg=-90, elbow_up=True)
    
    if result:
        print("\n" + "="*60)
        print("WORLD ANGLES (for kinematic calculations):")
        for joint, angle in result['world_angles'].items():
            print(f"  {joint}: {angle:7.2f}°")
        
        print("\n" + "="*60)
        print("SERVO COMMAND ANGLES (send these to your servos):")
        for joint, angle in result['servo_angles'].items():
            print(f"  {joint}: {angle:7.2f}°")
        
        # Verify
        print("\n" + "="*60)
        print("Verification:")
        result_pos = arm.forward_kinematics(result['servo_angles'], angle_type='servo')
        print(f"  Calculated position: ({result_pos[0]:.2f}, {result_pos[1]:.2f}, {result_pos[2]:.2f})")
        error = np.linalg.norm(np.array(result_pos) - np.array([target_x, target_y, target_z]))
        print(f"  Error: {error:.4f} mm")
        
    # Uncomment to run interactive calibration
    # arm.calibrate_joint('joint2')
