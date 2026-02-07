import numpy as np
import sys
import cv2

# You should replace these 3 lines with the output in calibration step
DIM=(640, 480)
K=np.array([[459.6897572664741, 0.0, 316.4286897895398], [0.0, 456.8325655024101, 232.55864201441727], [0.0, 0.0, 1.0]])
D=np.array([[-0.11894929009322144], [0.07473912474308911], [-0.003000594621484011], [-0.06340200069817385]])
def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)
