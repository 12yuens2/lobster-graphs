import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread("resized_lobster.JPG")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = np.float32(gray_image)


# Harris corner
dist = cv2.cornerHarris(gray_image, 2, 1, 0.001)
dist = cv2.dilate(dist, None)

harris_img = image.copy()
harris_img[dist>0.01*dist.max()] = [0, 0, 255]


# Shi-Tomasi corner
corners = cv2.goodFeaturesToTrack(gray_image, 30, 0.05, 1)
corners = np.int0(corners)

shi_tomasi_img = image.copy()
for i in corners:
    x,y = i.ravel()
    cv2.circle(shi_tomasi_img, (x,y), 3, 255, -1)

    
# SIFT
sift_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
sift = cv2.xfeatures2d.SIFT_create()
keypoints = sift.detect(sift_gray, None)

sift_image = image.copy()
sift_image = cv2.drawKeypoints(sift_gray, keypoints, sift_image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

keypoints, descriptors = sift.compute(sift_gray, keypoints)


# Show images
cv2.imshow("Harris", harris_img)
cv2.imshow("Shi-Tomasi", shi_tomasi_img)
cv2.imshow("SIFT", sift_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

