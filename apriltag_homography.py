import cv2
from pupil_apriltags import Detector
import numpy as np
import sys

def rectify_image_with_apriltag(image_path, tag_family='tag36h11', tag_size_pixels=100):
    """
    Rectifies an image based on a detected AprilTag, effectively creating a 
    top-down view of the tag and its immediate surroundings.

    :param image_path: Path to the input image.
    :param tag_family: The AprilTag family to detect (e.g., 'tag36h11').
    :param tag_size_pixels: The desired size of the tag in the rectified image.
    """
    # 1. Load Image and Detect AprilTag
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image {image_path}")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector = Detector(
            families=tag_family,
            nthreads=1,
            quad_decimate=1.0,
            quad_sigma=0.0,
            refine_edges=1,
            decode_sharpening=0.25,
            debug=0)
    results = detector.detect(gray)

    if not results:
        print("No AprilTag detected in the image.")
        return

    # Assume the first detected tag is the one we want to use
    tag = results[0]
    print(f"Detected Tag ID: {tag.tag_id}")

    # 2. Define Source and Destination Points
    # Source points are the corners of the detected tag in the original image
    src_points = tag.corners.astype(np.float32)

    # Destination points are the corners of the tag in the ideal, rectified image
    # We define a square of the desired size, ensuring the center aligns
    half_size = tag_size_pixels // 2
    # The order of corners in the tag is typically top-left, top-right, bottom-right, bottom-left
    dst_points = np.array([
        [-half_size, -half_size],
        [half_size, -half_size],
        [half_size, half_size],
        [-half_size, half_size]
    ], dtype=np.float32)
    # Shift points to start from the top-left corner (0, 0) of the new image
    dst_points += np.array([half_size, half_size])

    # 3. Compute Homography Matrix
    # The homography H maps src_points to dst_points
    H, _ = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 5.0)

    if H is None:
        print("Error: Could not compute homography.")
        return

    # 4. Apply Perspective Warp to Rectify the Image
    # Determine the size of the output image (large enough to see the tag clearly)
    # output_size = (tag_size_pixels, tag_size_pixels)
    output_size = (image.shape[1], image.shape[0])
    rectified_image = cv2.warpPerspective(image, H, output_size)

    # 5. Display or Save the Results
    cv2.imshow("Original Image", image)
    cv2.imshow("Rectified Image", rectified_image)
    cv2.imwrite("rectified_image.png", rectified_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example Usage:
# Replace 'your_image.jpg' with the path to your image containing an AprilTag.
# You can find sample tags on the [AprilRobotics GitHub](
if __name__ == '__main__':
    for p in sys.argv[1:]:
        rectify_image_with_apriltag(p)
