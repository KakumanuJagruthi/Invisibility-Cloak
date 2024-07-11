import cv2
import numpy as np

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Give the camera some time to warm up
import time

time.sleep(3)

# Capture the background (assuming it's static)
for i in range(30):
    ret, background = cap.read()

# Flip the background
background = np.flip(background, axis=1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame
    frame = np.flip(frame, axis=1)

    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the blue color range
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    # Create a mask to detect blue color
    mask1 = cv2.inRange(hsv, lower_blue, upper_blue)

    # Refine the mask
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    # Create an inverse mask
    mask2 = cv2.bitwise_not(mask1)

    # Segment out the blue color
    res1 = cv2.bitwise_and(frame, frame, mask=mask2)

    # Replace the blue color with the background
    res2 = cv2.bitwise_and(background, background, mask=mask1)

    # Combine the two results
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Display the output
    cv2.imshow('Magic Cloak', final_output)

    if cv2.waitKey(1) == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()
