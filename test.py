import cv2
import numpy as np

# Read an image from file
image = cv2.imread('path_to_image.jpg')

# Display the image in a window
cv2.imshow('Image Window', image)

# Wait for a key press indefinitely or for a specified amount of time (in milliseconds)
cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()
