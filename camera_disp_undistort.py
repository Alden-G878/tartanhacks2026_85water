import cv2
import numpy as np

# Get the optimal new camera matrix and region of interest
# The getOptimalNewCameraMatrix function is for the standard pinhole model,
# the fisheye model typically uses cv2.fisheye.estimateNewCameraMatrixForUndistort
# or directly undistort with scaling/cropping options.
# For simplicity here, we'll use a standard approach for the new matrix.
K = XXX
D = XXX
img_width, img_height = 640, 480 # Must match the resolution used in calibration

# You can adjust 'balance' from 0.0 (maximum zoom/crop) to 1.0 (keep all pixels, but might show black borders)
balance = 0.5 
new_K = cv2.fisheye.estimateNewCameraMatrixForUndistort(K, D, (img_width, img_height), np.eye(3), balance)

# --- 2. Setup Video Capture and Stream ---

# Open the default camera (change 0 to the correct index if you have multiple cameras)
cap = cv2.VideoCapture(0)

# Set resolution (must match or be proportional to calibration resolution)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_height)

if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    print("Camera opened successfully. Streaming...")

    while True:
        # Read a new frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # --- 3. Undistort the frame ---
        # Use cv2.fisheye.undistortImage with the new camera matrix
        undistorted_frame = cv2.fisheye.undistortImage(frame, K, D, Knew=new_K)

        # --- 4. Display the results ---
        cv2.imshow('Original Fisheye Stream', frame)
        cv2.imshow('Fisheye Corrected Stream', undistorted_frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

