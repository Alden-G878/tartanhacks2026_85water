import cv2
import numpy as np

# Define the lower and upper bounds of the color you want to detect in HSV
# Example for blue color (these values may need adjustment based on lighting)
lower_blue = np.array([100, 100, 100])
upper_blue = np.array([120, 255, 255])

# For a static image:
image = cv2.imread('your_image.png') # Replace with your image file
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a mask for the specified color range
mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

# Find contours in the mask
# Use the appropriate return values for your OpenCV version
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter and find the largest contour (optional, helps ignore noise)
if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    # Get the bounding box coordinates (x, y, width, height)
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Draw the bounding rectangle on the original image
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, "Blue Box", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the result
cv2.imshow("Detected Blue Box", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

