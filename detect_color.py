import cv2
import numpy as np
def find_src(red, green, blue):
    # Define the lower and upper bounds of the color you want to detect in HSV
    # Example for blue color (these values may need adjustment based on lighting)
    lower_blue = np.array([200, 170, 110])#([100, 100, 100]) #137, 195, 220
    upper_blue = np.array([230, 200, 140])#([140, 255, 255])
    
    lower_green = np.array([120, 150, 105])
    upper_green = np.array([140, 170, 125])
    
    lower_red = np.array([140, 140, 235])
    upper_red = np.array([160, 160, 255])
    if red:
        lower_blue = lower_red
        upper_blue = upper_red
    if green:
        lower_blue = lower_green
        upper_blue = upper_green
    
    # For a static image:
    image = cv2.imread('rectified_image.png')
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    cv2.imshow("hsv", hsv_image)
    cv2.waitKey(0)
    
    # Create a mask for the specified color range
    mask = cv2.inRange(image, lower_blue, upper_blue)
    
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
        print(f"x: {x*0.86487}, y: {y*0.86487}")
        cv2.putText(image, "Blue Box", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imshow("Detected Blue Box", image)
        cv2.putText(image, "Blue Box", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
 
        cv2.waitKey(0)
        return ((x+w/2)*0.86487,(y+h/2)*0.86487)
        cv2.putText(image, "Blue Box", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    else:
        print("Image recognition failed!")
    # Display the result
    cv2.imshow("Detected Blue Box", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

