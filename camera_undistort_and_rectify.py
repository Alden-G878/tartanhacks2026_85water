from "camera_disp_unsort.py"  import capture_and_undistort
from "apriltag_homography.py" import rectify_image_with_apriltag
if __name__ == '__main__':
    capture_and_undistort("img_udist.png")
    rectify_image_with_apriltag("img_udist.png")
