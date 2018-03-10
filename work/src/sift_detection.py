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
#kps = cc.get_image_kps(filename)

all_image = cc.drawKeypoints(filename, all_kps)
image = cc.drawKeypoints(filename, kps)

'''
save_histogram(image, kps[1], "claw.hist")
save_histogram(image, kps[2], "arm.hist")
save_histogram(image, kps[13], "head.hist")
save_histogram(image, kps[18], "body.hist")
save_histogram(image, kps[40], "back.hist")
save_histogram(image, kps[50], "tail.hist")
'''

#np.save("part.hist", hist)

#print("Write to gdf")
#write_to_gdf(kps, str(image_file) + ".gdf", "graphs/")

print("Write image with keypoints")
annotated_image = image.copy()
for i in range(len(kps)):
    kp = kps[i]
    pos = cc.get_point_tuple(kp)
    cv2.putText(annotated_image, str(i) + ": " + str(int(kp.size)), pos, 1, 3, (0,0,255), 2, cv2.LINE_AA)

cw.write_image(annotated_image, "after.JPG")
cw.write_image(all_image, "before.JPG")



'''
j = 0
for image_file in os.listdir(images_path):
    image_filename = images_path + image_file
    image = cv2.imread(image_filename)

    print("Read image " + image_file)
    kps = get_keypoints(image_filename)


    # Write to graph file format
    write_to_gdf(kps,str(image_file)+".gdf")

    # Draw keypoints
    sift_image = image.copy()

    # Draw keypoint information
    hist = np.load("lobster.hist.npy")
    hist.reshape(256,256,256)

            
    sift_image = cv2.drawKeypoints(sift_image, kps, sift_image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

     
    #cv2.namedWindow("Unfiltered" + str(j), cv2.WINDOW_NORMAL)
    #cv2.imshow("Unfiltered" + str(j), sift_image)


    correl_kps = filter_keypoints_histogram(sift_image, hist, kps, method=cv2.HISTCMP_CORREL)
    filtered_image = drawKeypoints(image.copy(), [kp for kp,diff in correl_kps])
    #cv2window("Filtered correl" + str(j), filtered_image)
    
    for kp,diff in correl_kps:
        pos = get_point_tuple(kp)
        cv2.putText(filtered_image, str(int(kp.size))+": "+str(diff), pos, 1, 1, (0,0,255), 2, cv2.LINE_AA)

    cv2.imwrite("imgs/keypoints/"+image_file, filtered_image)
    print("Wrote " + image_file)

    j += 1

cv2.waitKey(0)
cv2.destroyAllWindows()

'''
