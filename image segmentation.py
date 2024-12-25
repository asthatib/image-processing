import cv2
import numpy as np

# Usage
def solution(image_path):
    image = cv2.imread(image_path)
    smooth_image = cv2.GaussianBlur(image, (15, 15), 0)
    image_hsv = cv2.cvtColor(smooth_image, cv2.COLOR_BGR2HSV)

    #Find circles to denote sun and return back image is circle is detected
    edges = cv2.Canny(image_hsv, 50, 150, apertureSize=3)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=12)
    if circles is not None:
        black_image = np.zeros_like(image)
        return black_image
    
    color_lower = np.array([0, 135, 135])
    color_upper = np.array([40, 255, 255])
    color_mask = cv2.inRange(image_hsv, color_lower, color_upper)
    erosion_kernel = np.ones((5, 5), np.uint8)
    refined_mask = cv2.erode(color_mask, erosion_kernel, iterations=1)
    segmented_image = np.zeros_like(image)
    segmented_image[refined_mask > 0] = [255, 255, 255]

    return segmented_image