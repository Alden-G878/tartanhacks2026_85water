import cv2
import os

# Create a directory to save images if it doesn't exist
output_dir = "calib_img"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the default camera (device index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

img_counter = 0

while True:
    # Read a frame from the stream
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    # Display the resulting frame
    cv2.imshow("Stream Preview", frame)

    # Wait for a key press
    k = cv2.waitKey(1)
    
    # Check for 'ESC' key press (ASCII 27) to exit the program
    if k % 256 == 27:
        print("Escape hit, closing...")
        break
    
    # Check for 'SPACE' key press (ASCII 32) to save an image
    elif k % 256 == 32:
        img_name = os.path.join(output_dir, f"opencv_frame_{img_counter}.png")
        # Save the current frame as a PNG file
        cv2.imwrite(img_name, frame)
        print(f"{img_name} saved!")
        img_counter += 1

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

