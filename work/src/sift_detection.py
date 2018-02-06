import sys
import os
import cv2
import numpy as np

def closest_kp(keys, des, descriptor):
    lowest = 1000000
    best_kp = 0

    for i in range(len(keys)):
        distance = cv2.norm(descriptor, des[i])
        if distance < lowest:
            lowest = distance
            best_kp = keys[i]

    return best_kp 

def best_body_kp(key_dict):

    #Sort of keypoint size as body should be largest keypoint
    key_dict = sorted(key_dict.items(), key=lambda x: x[0].size, reverse=True)
    keys = [k for k,v in key_dict]
    des = [v for k,v in key_dict]

    body_descriptor = np.fromfile("body.kp", dtype=np.float32)

    return closest_kp(keys[:3], des, body_descriptor)




images_path = "imgs/lobsters/"
images = []

for image_file in os.listdir(images_path):
    image = cv2.imread(images_path + image_file)
    
    #h, w = image.shape[:2]
    #image = cv2.resize(image, (int(0.3*w), int(0.3*h)), interpolation=cv2.INTER_CUBIC)
    
    #resize?
    print(image_file)
    images.append(image)

'''
image = cv2.imread(images_path + "IMG_1380.JPG")
h, w = image.shape[:2]
for i in range(1,9):
    scale = i * 1.0 / 10
    images.append(cv2.resize(image, (int(scale*w), int(scale*h)), interpolation=cv2.INTER_CUBIC))
'''

sift = cv2.xfeatures2d.SIFT_create()


j = 0
body_kp = 0
for image in images:
    sift_kps = sift.detect(image, None)
    sift_image = image.copy()

    keys, des = sift.compute(sift_image, sift_kps)
    key_dict = dict(zip(keys, des))
    kps = []

    # Best body keypoint
    kps.append(best_body_kp(key_dict))
    ''' 
    for kp in sift_kps:
        distance = cv2.norm(kp
        if kp.size > 20:
            kps.append(kp)
    kps.sort(key = lambda x: x.response, reverse=True)
    '''


    sift_image = cv2.drawKeypoints(image, kps, sift_image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    c1 = (0,0)
    index = 0
    for kp in kps:
        c2 = (int(kp.pt[0]), int(kp.pt[1]))
        #cv2.line(sift_image, c1, c2, (0,255,0), 5)

        cv2.putText(sift_image, str(int(kp.size))+": "+str(kp.response), c2, 1, 1, (0,0,255), 2, cv2.LINE_AA)
        c1 = c2
        index += 1

    h, w = sift_image.shape[:2]

    cv2.namedWindow("Image " + str(j), cv2.WINDOW_NORMAL)
    cv2.imshow("Image " + str(j), sift_image)
    j += 1

cv2.waitKey(0)
cv2.destroyAllWindows()

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

'''
