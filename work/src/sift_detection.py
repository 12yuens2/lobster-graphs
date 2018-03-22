import sys
import os
import cv2
import numpy as np

import common.matching as cm
import common.cv as cc
import common.write as cw

""" sift_detection.py: Draw keypoints on top of the lobster image and write keypoints to gdf graph format """

def save_histogram(image, kp, filename):
    hist = cc.get_histogram(image, kp)
    np.save("hists/" + filename, hist)

filename = sys.argv[1]

all_kps = cc.get_all_keypoints(filename)
kps = cc.get_image_kps(filename)
#kps = cc.get_all_keypoints(filename)

all_image = cc.drawKeypoints(filename, all_kps)
image = cc.drawKeypoints(filename, kps)

'''
save_histogram(all_image, all_kps[1], "claw.hist")
save_histogram(all_image, all_kps[2], "arm.hist")
save_histogram(all_image, all_kps[13], "head.hist")
save_histogram(all_image, all_kps[18], "body.hist")
save_histogram(all_image, all_kps[40], "back.hist")
save_histogram(all_image, all_kps[50], "tail.hist")
'''

kps = cc.remove_duplicates(kps)

print("Write image with keypoints")
annotated_image = image.copy()
for i in range(len(kps)):
    kp = kps[i]
    pos = cc.get_point_tuple(kp)
    cv2.putText(annotated_image, str(i) + ": " + str(int(kp.size)), pos, 1, 3, (0,0,255), 2, cv2.LINE_AA)

cw.write_image(annotated_image, "after.JPG")
cw.write_image(all_image, "before.JPG")
