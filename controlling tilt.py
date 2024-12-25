import cv2
import numpy as np


def solution(image_path):
    img= cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,binary = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    corner_points=[]
    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            corner_points = approx
    centroid = np.mean(corner_points, axis=0)[0]

    angles = np.arctan2(corner_points[:, 0, 1] - centroid[1], corner_points[:, 0, 0] - centroid[0])
    corner_points = corner_points[np.argsort(angles)]
    des_width = 600  
    des_height = 600  
    desired_corners = np.array([[0, 0], [des_width, 0], [des_width, des_height], [0, des_height]], dtype='float32')
    corner_points = np.array(corner_points,dtype=np.float32)
    desired_corners = np.array(desired_corners,dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(corner_points, desired_corners)

    corr_image = cv2.warpPerspective(img, matrix, (des_width, des_height))
    answer = cv2.cvtColor(corr_image, cv2.COLOR_BGR2RGB)
    return(answer)