import cv2
import numpy as np

# Get the optimal new camera matrix and region of interest
# The getOptimalNewCameraMatrix function is for the standard pinhole model,
# the fisheye model typically uses cv2.fisheye.estimateNewCameraMatrixForUndistort
# or directly undistort with scaling/cropping options.
# For simplicity here, we'll use a standard approach for the new matrix.
# DIM=(640, 480)
def capture_and_undistort(img_name):
    K=np.array([[459.50075535511127, 0.0, 315.4093020757232], [0.0, 456.5667192722284, 232.44968716323072], [0.0, 0.0, 1.0]])
    D=np.array([[-0.11675163361043045], [0.07398723179179927], [-0.01466585277138975], [-0.047624989531767185]])
    img_width, img_height = 640, 480 # Must match the resolution used in calibration

    # You can adjust 'balance' from 0.0 (maximum zoom/crop) to 1.0 (keep all pixels, but might show black borders)
    balance = 0.5 
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, (img_width, img_height), np.eye(3), balance)

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
            else:
                print("Captured image")
    
            # --- 3. Undistort the frame ---
            # Use cv2.fisheye.undistortImage with the new camera matrix
            undistorted_frame = cv2.fisheye.undistortImage(frame, K, D, Knew=new_K)
            print("Undisorited capture")
            # --- 4. Display the results ---
            #cv2.imshow('Original Fisheye Stream', frame)
            #cv2.imshow('Fisheye Corrected Stream', undistorted_frame)
    
            # Break the loop when 'q' key is pressed
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
            #if cv2.waitKey(1) & 0xFF == ord(' '):
            #    cv2.imwrite("img_udst.png", undistorted_frame)
            #    print("saved frame to img_udst.png")
            cv2.imwrite(img_name, undistorted_frame)
            print(f"Wrote undistorted image to {img_name}")
            break;
        # Release the capture and close windows
        cap.release()
        cv2.destroyAllWindows()

