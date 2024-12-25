import cv2
import numpy as np

# Function to crop out the white space from an image
def auto_crop_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Assuming the largest external contour in image is the object to keep
    largest_contour = max(contours, key=cv2.contourArea)
    # Getting the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

# Solution function to find if given ravana is real or fake
def solution(image_path):
    image=auto_crop_image(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY)
    height, width = threshold_image.shape
    left_bound=0
    right_bound=0

    #Finding the middlemost point of the object
    grayscale_column = np.column_stack(np.where(gray_image[-1, :] < 255))
    middle_point = 0
    if grayscale_column.shape[0] > 0:
        middle = (grayscale_column[0] + grayscale_column[-1]) // 2
        middle_point = middle[0]

    #Finding the leftmost boundary of the object
    for col in range(width):
        for row in range(height - 1, -1, -1):
            pixil = threshold_image[row, col]
            if pixil== 0:
                left_bound = col
                break

        if pixil == 0:
            break

    #Findind the rightmost boundary of the image
    for col in range(width - 1, -1, -1):
        for row in range(height - 1, -1, -1):
            pixil = threshold_image[row, col]
            if pixil == 0 :
                right_bound = col
                break

        if pixil == 0:
            break
    
    #Determine if the object is real or fake by comparing length of non-white pixils
    if(middle_point - left_bound >= right_bound - middle_point -10):
        return "fake"
    else:
        return "real"
