import sys
import os
import cv2
import numpy as np


'''
images_path = "imgs/lobsters/"
images = []
for image_file in os.listdir(images_path):
    image = cv2.imread(images_path + image_file)
    h, w = image.shape[:2]
    image = cv2.resize(image, (int(0.3*w), int(0.3*h)), interpolation=cv2.INTER_CUBIC)
    #resize?
    
    images.append(cv2.imread(images_path + image_file))

'''
image = cv2.imread("imgs/lobsters/IMG_1388.JPG")
h, w  = image.shape[:2]
image = cv2.resize(image, (int(0.4*w), int(0.4*h)), interpolation=cv2.INTER_CUBIC)


sift = cv2.xfeatures2d.SIFT_create()
kps = sift.detect(image, None)

sift_image = image.copy()
sift_image = cv2.drawKeypoints(image, kps, sift_image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.namedWindow("SIFT", cv2.WINDOW_NORMAL)
cv2.imshow("SIFT", sift_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
