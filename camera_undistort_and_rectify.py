import camera_disp_undistort
import apriltag_homography
if __name__ == '__main__':
    camera_disp_undistort.capture_and_undistort("img_udist.png")
    apriltag_homography.rectify_image_with_apriltag("img_udist.png")
