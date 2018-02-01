import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread("imgs/IMG_5432.JPG")
h, w = image.shape[:2]
image = cv2.resize(image, (int(0.3*w), int(0.3*h)), interpolation=cv2.INTER_CUBIC)

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


# SURF
surf = cv2.xfeatures2d.SURF_create(10000)
surf_gray = image.copy() 
surf_kps, surf_des = surf.detectAndCompute(surf_gray, None)

surf_image = image.copy()
surf_image = cv2.drawKeypoints(surf_gray, surf_kps, None, (255,0,0), 4)


# BRIEF
brief_image = image.copy()

brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()

brief_kps = sift.detect(brief_image, None)
brief_kps, brief_des = brief.compute(brief_image, brief_kps)

#print(brief.getInt("bytes"))
print(brief_des.shape)


# Show images
cv2.imshow("Harris", harris_img)
cv2.imshow("Shi-Tomasi", shi_tomasi_img)
cv2.imshow("SIFT", sift_image)
cv2.imshow("SURF", surf_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

