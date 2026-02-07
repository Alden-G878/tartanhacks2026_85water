import numpy as np
from typing import Tuple, Optional

class RobotArmIK:
    def __init__(self):
        """Initialize robot arm with segment lengths in mm"""
        self.h_base = 96.1      # Base/shoulder height
        self.L1 = 90.6          # Shoulder to elbow
        self.L2 = 90.6          # Elbow to wrist
        self.L3 = 144.57        # Wrist to grabber
        
    def inverse_kinematics(self, 
                          x: float, 
                          y: float, 
                          z: float, 
                          grabber_angle_deg: float = -90.0,
                          elbow_up: bool = True) -> Optional[Tuple[float, float, float, float]]:
        """
        Calculate inverse kinematics for 4-DOF arm.
        
        Args:
            x: Target x position (mm) - forward/back from base
            y: Target y position (mm) - left/right from base
            z: Target z position (mm) - height above ground
            grabber_angle_deg: Desired angle of grabber relative to horizontal (degrees)
                              -90 = pointing straight down (typical for grabbing from above)
            elbow_up: If True, use elbow-up configuration; if False, use elbow-down
            
        Returns:
            Tuple of (theta1, theta2, theta3, theta4) in degrees, or None if unreachable
            theta1: Base rotation
            theta2: Shoulder angle
            theta3: Elbow angle
            theta4: Wrist angle
        """
        
        # Convert grabber angle to radians
        grabber_angle = np.deg2rad(grabber_angle_deg)
        
        # Step 1: Calculate base rotation (theta1)
        theta1 = np.arctan2(y, x)
        
        # Step 2: Calculate horizontal reach distance
        r_target = np.sqrt(x**2 + y**2)
        
        # Step 3: Calculate wrist position (work backwards from grabber)
        # The grabber extends from the wrist at the specified angle
        r_wrist = r_target - self.L3 * np.cos(grabber_angle)
        z_wrist = z - self.L3 * np.sin(grabber_angle)
        
        # Step 4: Solve 2-link IK for shoulder and elbow
        # Distance from shoulder to wrist in the vertical plane
        z_from_shoulder = z_wrist - self.h_base
        d = np.sqrt(r_wrist**2 + z_from_shoulder**2)
        
        # Check if target is reachable
        if d > (self.L1 + self.L2) or d < abs(self.L1 - self.L2):
            print(f"Target unreachable: distance {d:.2f}mm, max reach {self.L1 + self.L2:.2f}mm")
            return None
        
        # Calculate elbow angle using law of cosines
        cos_theta3 = (d**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        
        # Clamp to [-1, 1] to handle numerical errors
        cos_theta3 = np.clip(cos_theta3, -1.0, 1.0)
        
        if elbow_up:
            theta3 = np.arccos(cos_theta3)  # Positive angle (elbow up)
        else:
            theta3 = -np.arccos(cos_theta3)  # Negative angle (elbow down)
        
        # Calculate shoulder angle
        alpha = np.arctan2(z_from_shoulder, r_wrist)
        beta = np.arctan2(self.L2 * np.sin(theta3), self.L1 + self.L2 * np.cos(theta3))
        theta2 = alpha - beta
        
        # Step 5: Calculate wrist angle to achieve desired grabber angle
        # The sum of all joint angles determines the final grabber orientation
        theta4 = grabber_angle - theta2 - theta3
        
        # Convert all angles to degrees for output
        return (np.rad2deg(theta1), 
                np.rad2deg(theta2), 
                np.rad2deg(theta3), 
                np.rad2deg(theta4))
    
    def forward_kinematics(self, theta1_deg: float, theta2_deg: float, 
                          theta3_deg: float, theta4_deg: float) -> Tuple[float, float, float]:
        """
        Calculate end effector position from joint angles (for verification).
        
        Args:
            theta1_deg, theta2_deg, theta3_deg, theta4_deg: Joint angles in degrees
            
        Returns:
            Tuple of (x, y, z) position of grabber tip in mm
        """
        # Convert to radians
        theta1 = np.deg2rad(theta1_deg)
        theta2 = np.deg2rad(theta2_deg)
        theta3 = np.deg2rad(theta3_deg)
        theta4 = np.deg2rad(theta4_deg)
        
        # Calculate in vertical plane first
        # Shoulder position
        z_shoulder = self.h_base
        r_shoulder = 0
        
        # Elbow position
        r_elbow = r_shoulder + self.L1 * np.cos(theta2)
        z_elbow = z_shoulder + self.L1 * np.sin(theta2)
        
        # Wrist position
        r_wrist = r_elbow + self.L2 * np.cos(theta2 + theta3)
        z_wrist = z_elbow + self.L2 * np.sin(theta2 + theta3)
        
        # Grabber position
        grabber_angle = theta2 + theta3 + theta4
        r_grabber = r_wrist + self.L3 * np.cos(grabber_angle)
        z_grabber = z_wrist + self.L3 * np.sin(grabber_angle)
        
        # Convert from cylindrical to cartesian coordinates
        x = r_grabber * np.cos(theta1)
        y = r_grabber * np.sin(theta1)
        z = z_grabber
        
        return (x, y, z)


# Example usage
if __name__ == "__main__":
    arm = RobotArmIK()
    
    # Example: Grab an object at position (200, 100, 10) mm
    # with grabber pointing straight down
    target_x = 127.0  # mm forward
    target_y = 10.0  # mm to the side
    target_z = 10.0   # mm above ground (height of paper surface)
    
    print("Target position:", (target_x, target_y, target_z))
    
    # Calculate joint angles
    angles = arm.inverse_kinematics(target_x, target_y, target_z, 
                                    grabber_angle_deg=-90, elbow_up=True)
    
    if angles:
        theta1, theta2, theta3, theta4 = angles
        print(f"\nJoint angles (degrees):")
        print(f"  Base (θ1):     {theta1:7.2f}°")
        print(f"  Shoulder (θ2): {theta2:7.2f}°")
        print(f"  Elbow (θ3):    {theta3:7.2f}°")
        print(f"  Wrist (θ4):    {theta4:7.2f}°")
        
        # Verify with forward kinematics
        result_pos = arm.forward_kinematics(theta1, theta2, theta3, theta4)
        print(f"\nVerification (forward kinematics):")
        print(f"  Calculated position: ({result_pos[0]:.2f}, {result_pos[1]:.2f}, {result_pos[2]:.2f})")
        print(f"  Error: {np.linalg.norm(np.array(result_pos) - np.array([target_x, target_y, target_z])):.4f} mm")
    else:
        print("Target is unreachable!")
    
    # Try elbow-down configuration
    print("\n" + "="*50)
    print("Trying elbow-down configuration:")
    angles_down = arm.inverse_kinematics(target_x, target_y, target_z, 
                                        grabber_angle_deg=-90, elbow_up=False)
    if angles_down:
        theta1, theta2, theta3, theta4 = angles_down
        print(f"  Base (θ1):     {theta1:7.2f}°")
        print(f"  Shoulder (θ2): {theta2:7.2f}°")
        print(f"  Elbow (θ3):    {theta3:7.2f}°")
        print(f"  Wrist (θ4):    {theta4:7.2f}°")
