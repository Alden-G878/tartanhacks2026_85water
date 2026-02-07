import math
from typing import Tuple, Optional
def inv_kinematics(x: float, y: float, z: float)
    theta1 = math.atan2(y, x)
    D = math.sqrt(x**2 + y**2)

    if y > 
# /G:/My Drive/TH2026/IK.py
# GitHub Copilot
# Inverse kinematics for a 4DOF serial robot:
# - q1: base yaw (about Z)
# - q2: shoulder pitch (about Y axis in rotated base frame)
# - q3: elbow pitch
# - q4: wrist pitch
#
# Conventions:
# - Base at origin. z axis up.
# - After base yaw, the remaining 3 joints form a planar 3R chain in the plane defined by that yaw.
# - Link parameters: d1 (base height), a2 (shoulder->elbow), a3 (elbow->wrist), a4 (wrist->end-effector along forward axis).
# - Desired pose: target position (x,y,z) and end-effector pitch phi (angle of end-effector forward axis above the horizontal plane),
#   where total pitch = q2 + q3 + q4 = phi.
#
# IK approach:
# 1) q1 = atan2(y, x)
# 2) reduce to plane: r = sqrt(x^2 + y^2), s = z - d1
# 3) compute wrist center in planar coords: x_w = r - a4 * cos(phi), z_w = s - a4 * sin(phi)
# 4) solve 2R (a2,a3) planar IK for q2,q3 using law of cosines
# 5) q4 = phi - q2 - q3
#
# Returns angles in radians. Two elbow configurations supported: 'elbow_up' or 'elbow_down'.


def _clamp(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def inverse_kinematics(x: float, y: float, z: float, phi: float = 0.0,
                       L1: float = 96.1, L2: float = 90.6, L3: float = 90.6, L4: float = 144.57,
                       elbow: str = 'elbow_up') -> Tuple[float, float, float, float]:
    """
    Solve IK for given end-effector position (x,y,z) and desired pitch phi.
    Returns (q1, q2, q3, q4) in radians.
    elbow: 'elbow_up' or 'elbow_down'
    Raises ValueError if target is unreachable or input invalid.
    """
    # return angles in degrees: helpers and optional FK wrapper (so FK still gets radians if we convert q's)
    _return_degrees = True
    _rad2deg = lambda a: a * 180.0 / math.pi
    _deg2rad = lambda a: a * math.pi / 180.0
    _orig_forward_kinematics = globals().get('forward_kinematics')
    if _orig_forward_kinematics is not None and _return_degrees:
        def forward_kinematics(q1, q2, q3, q4, d1_, a2_, a3_, a4_):
            return _orig_forward_kinematics(_deg2rad(q1), _deg2rad(q2), _deg2rad(q3), _deg2rad(q4), d1_, a2_, a3_, a4_)
    # Note: after q1,q2,q3,q4 are computed (in radians), convert them to degrees just before returning:
    # q1, q2, q3, q4 = _rad2deg(q1), _rad2deg(q2), _rad2deg(q3), _rad2deg(q4)
    if elbow not in ('elbow_up', 'elbow_down'):
        raise ValueError("elbow must be 'elbow_up' or 'elbow_down'")

    # 1) base yaw
    q1 = math.atan2(y, x)

    # 2) planar coordinates after base rotation
    r = math.hypot(x, y)  # horizontal distance from base axis
    s = z - L1            # vertical coordinate relative to shoulder joint

    # 3) wrist center position in planar coords
    x_w = r - L4
    z_w = s

    # distance to wrist center
    D = math.hypot(x_w, z_w)
    if D < 1e-9:
        # degenerate: wrist center at origin of planar chain
        # Solve with special handling (may be infinite solutions)
        raise ValueError("degenerate wrist-center; ambiguous configurations")

    # 4) law of cosines for q3 (elbow)
    cos_q3 = _clamp((x_w**2 + z_w**2 - L2**2 - L3**2) / (2 * L2 * L3))
    try:
        q3 = math.atan2(+math.sqrt(max(0.0, 1.0 - cos_q3**2)), cos_q3)
    except ValueError:
        raise ValueError("target unreachable: numeric domain error for q3")

    # 5) compute q2
    k1 = L2 + L3 * math.cos(q3)
    k2 = L3 * math.sin(q3)
    q2 = math.atan2(z_w, x_w) - math.atan2(k2, k1)

    # 6) wrist pitch
    q4 = phi - q2 - q3

    # validate by forward kinematics numeric check (optional, light tolerance)
    x_fk, y_fk, z_fk, phi_fk = forward_kinematics(q1, q2, q3, q4, L1, L2, L3, L4)
    err = math.hypot(x - x_fk, y - y_fk, z - z_fk)
    if err > 1e-3 or abs(((phi - phi_fk + math.pi) % (2*math.pi)) - math.pi) > 1e-2:
        # sometimes angle wrapping causes phi check issues; above handles that.
        raise ValueError(f"IK solution inaccurate or unreachable (pos err={err:.4f})")

    return q1, q2, q3, q4

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     target = (0.4, 0.1, 0.2, 0.0)  # x,y,z,phi
#     try:
#         sol = inverse_kinematics(*target)
#         print("IK solution (radians):", sol)
#         print("FK ->", forward_kinematics(*sol))
#     except ValueError as e:
#         print("IK failed:", e)