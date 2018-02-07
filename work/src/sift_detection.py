import sys
import os
import cv2
import math
import numpy as np

def closest_kp(keys, des, descriptor):
    lowest = 1000000
    best_kp = 0

    print(descriptor.shape)
    print(des[0].shape)
    
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

    body_descriptor = np.fromfile("body.kp", dtype=np.uint8)

    return closest_kp(keys[:3], des, body_descriptor)

def get_distance(kp1, kp2):
    pt1 = kp1.pt
    pt2 = kp2.pt
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

def get_point_tuple(kp):
    return (int(kp.pt[0]), int(kp.pt[1]))

def midpoint(kp1, kp2):
    pt1 = get_point_tuple(kp1)
    pt2 = get_point_tuple(kp2)

    print("pt1: " + str(pt1))
    print("pt2: " + str(pt2))
    
    return (int((pt1[0] + pt2[0]) / 2), int((pt1[1] + pt2[1]) / 2)) 


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
#sift = cv2.ORB_create()

j = 0
body_kp = 0
for image in images:
    sift_kps = sift.detect(image, None)
    sift_image = image.copy()

    keys, des = sift.compute(sift_image, sift_kps)
    key_dict = dict(zip(keys, des))
    kps = []

    # Best body keypoint
    #kps.append(best_body_kp(key_dict))

    # Filter keypoints
    for kp in sift_kps:
        octave = kp.octave & 0xFF
        if octave > 3 and octave < 8:
            kps.append(kp)
    kps.sort(key = lambda x: x.response, reverse=True)


    # Draw keypoints
    sift_image = cv2.drawKeypoints(image, kps, sift_image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Draw keypoint information
    c1 = (0,0)
    index = 0
    for kp in kps:
        c2 = get_point_tuple(kp)
        #cv2.line(sift_image, c1, c2, (0,255,0), 5)

        cv2.putText(sift_image, str(int(kp.size))+": "+str(index), c2, 1, 1, (0,0,255), 2, cv2.LINE_AA)
        c1 = c2
        index += 1

    

    cv2.line(sift_image, get_point_tuple(kps[12]), get_point_tuple(kps[6]), (0,0,255), thickness=4)

    text = str(get_distance(kps[12], kps[6]))
    point = midpoint(kps[12], kps[6])
    print(point)
    cv2.putText(sift_image, text, point, 1, 1, (0,0,255), 2, cv2.LINE_AA)
 
        
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
