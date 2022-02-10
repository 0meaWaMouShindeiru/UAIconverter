from scipy.spatial.transform import Rotation


def convert_Euler_to_quaternion(yaw, pitch, roll):
    # extrinsic(xyz) vs intrinsic (XYZ) -> should be discussed
    # improvement: XYZ could also be moved to config
    rotation = Rotation.from_euler('YZX', [yaw, pitch, roll], degrees=True)
    # from documentation: The returned value is in scalar-last (x, y, z, w) format.
    return tuple(rotation.as_quat())
