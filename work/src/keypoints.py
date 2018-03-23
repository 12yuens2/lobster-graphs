import sys
import cv2
import numpy as np

def draw_keypoints(image, kps, scale):
    img = image.copy()
    img = cv2.resize(image, (0,0), fx=scale, fy=scale)

    for kp in kps:
        (x,y) = kp.pt
        x *= scale
        y *= scale

        kp.pt = (x,y)
        kp.size *= scale

    img = cv2.drawKeypoints(img, kps, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return img
    

def harris(gray, image):
    dist = cv2.cornerHarris(gray, 2, 29, 0.0001)
    dist = cv2.dilate(dist, None)

    harris_img = image.copy()
    harris_img[dist>0.001*dist.max()] = [0,0,255]

    return harris_img

def shi_tomasi(gray_image, image):
    corners = cv2.goodFeaturesToTrack(gray_image, 500, 0.01, 1)
    corners = np.int0(corners)

    shi_tomasi_img = image.copy()
    for i in corners:
        x,y = i.ravel()
        cv2.circle(shi_tomasi_img, (x,y), 10, (0,0,255), -1)

    return shi_tomasi_img

def sift(image):
    sift = cv2.xfeatures2d.SIFT_create()
    sift_kps = sift.detect(image, None)

    return draw_keypoints(image, sift_kps, 0.2)

def surf(image):
    surf = cv2.xfeatures2d.SURF_create(2000)
    surf_kps = surf.detect(image, None)

    return draw_keypoints(image, surf_kps, 0.2)

def orb(image):
    orb = cv2.ORB_create()
    orb_kps = orb.detect(image, None)

    return draw_keypoints(image, orb_kps, 0.2)


#image_file = "IMG_5298.JPG"
image_file = sys.argv[1]
image = cv2.imread("imgs/lobsters/" + image_file)
#h, w = image.shape[:2]

gray_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
gray_image = np.float32(gray_image)


# Harris corner
harris_img = harris(gray_image, image)
cv2.imwrite("img-harris2.png", harris_img)

# Shi-Tomasi corner
shi_tomasi_img = shi_tomasi(gray_image, image)
cv2.imwrite("img-shi-tomasi2.png", shi_tomasi_img)

# SIFT
sift_img = sift(image)
cv2.imwrite("img-sift2.png", sift_img)

# SURF
surf_img = surf(image)
cv2.imwrite("img-surf2.png", surf_img)

# ORB
orb_img = orb(image)
cv2.imwrite("img-orb2.png", orb_img)



