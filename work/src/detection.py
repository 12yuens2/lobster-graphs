import os
import subprocess
import cv2
import numpy as np
import sys


import common.matching as cm
import common.cv as cc
import common.write as cw




def get_detected_image(image, kps):
    for i in range(len(kps)):
        kp = kps[i]
        cv2.putText(image, str(i), cc.get_point_tuple(kp), 1, 1, (0,0,255), 2, cv2.Line_AA)

    return image

def write_detected_image(read_path, write_path, kps):
    image = cv2.imread(read_path)
    cv2.drawKeypoints(image, kps, image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    for i in range(len(kps)):
        kp = kps[i]
        cv2.putText(image, str(i+1), cc.get_point_tuple(kp), 1, 4, (0,0,255), 2, cv2.LINE_AA)
    cv2.imwrite(write_path, image)

    

category: str = sys.argv[1]
read_path = "imgs/dataset/" + category + "/raw/"
write_path = "imgs/dataset/" + category + "/detected/"



for image_file in os.listdir(read_path):
    print(image_file)
    kps = cc.get_image_kps(read_path + image_file)
    #cw.kps_as_gdf(kps, image_file[4:8] + ".gdf", "graphs/annotated/" + category + "/")

    write_detected_image(read_path + image_file, write_path + image_file, kps)



#annotated to complete
# tranlate_graph() gfu -> Graph
# graph_to_gdf() Graph -> gfu

