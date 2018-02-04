import cv2
import numpy as np

image = cv2.imread("imgs/lobsters/IMG_4720.JPG")
h, w = image.shape[:2]

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

image = cv2.resize(image, (int(0.1*w), int(0.1*h)), interpolation=cv2.INTER_CUBIC)
sift_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
sift = cv2.xfeatures2d.SIFT_create()
sift_kps = sift.detect(sift_gray, None)

good_kps = []
for kp in sift_kps:
    if kp.size > 1:
        good_kps.append(kp)

sift_image = image.copy()
sift_image = cv2.drawKeypoints(sift_gray, good_kps, sift_image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

keypoints, descriptors = sift.compute(sift_gray, good_kps)


# SURF
surf = cv2.xfeatures2d.SURF_create(10000)
surf_gray = image.copy() 
surf_kps, surf_des = surf.detectAndCompute(surf_gray, None)

# Sort by highest response in keypoints
surf_kps.sort(key = lambda x: x.response, reverse=True)

surf_image = image.copy()
surf_image = cv2.drawKeypoints(surf_gray, surf_kps[:10], None, (255,0,0), 4)

print("SURF keypoints: " + str(len(surf_kps)))
for kp in surf_kps[:10]:
    print(str(kp.response))

print(type(surf_des[0]))

# BRIEF
brief_image = image.copy()

brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()

brief_kps = sift.detect(brief_image, None)
brief_kps, brief_des = brief.compute(brief_image, brief_kps)

#print(brief.getInt("bytes"))
print(brief_des.shape)


# Show images
cv2.namedWindow("SIFT", cv2.WINDOW_NORMAL)
#cv2.imshow("Harris", harris_img)
#cv2.imshow("Shi-Tomasi", shi_tomasi_img)
cv2.imshow("SIFT", sift_image)
#cv2.imshow("SURF", surf_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

