import cv2
import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny
from skimage import io

def detect_text_orientation(image_path):
    img = io.imread(image_path, as_gray=True)
    #using canny to detect edges
    edges = canny(img, sigma=2)
    #apply hough transform
    h, theta, d = hough_line(edges)
    _, angle, _ = hough_line_peaks(h, theta, d)
    angle_degrees = np.rad2deg(angle)[0] + 90
    return angle_degrees

def solution(image_path):
    img = cv2.imread(image_path)
    rotation_angle = detect_text_orientation(image_path)
    height, width = img.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), rotation_angle, 1)
    new_width = int(width * np.abs(np.cos(np.radians(rotation_angle))) + height * np.abs(np.sin(np.radians(rotation_angle))))
    new_height = int(height * np.abs(np.cos(np.radians(rotation_angle))) + width * np.abs(np.sin(np.radians(rotation_angle))))
    dx = (new_width - width) // 2
    dy = (new_height - height) // 2
    #now apply padding so that the corners dont get cut
    padded_image = cv2.copyMakeBorder(img, dy, dy, dx, dx, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    rotated_image = cv2.warpAffine(padded_image, rotation_matrix, (new_width, new_height), flags=cv2.INTER_LINEAR, borderMode = cv2.BORDER_CONSTANT, borderValue = (255, 255, 255))
    return rotated_image


