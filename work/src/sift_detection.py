import sys
import os
import cv2
from common_cv import *

""" sift_detection.py: Draw keypoints on top of the lobster image and write keypoints to gdf graph format """



images_path = "imgs/dither/"
images = []


for image_file in os.listdir(images_path):
    filename = images_path + image_file
    kps = get_image_kps(filename)
    image = drawKeypoints(filename, kps)
    
    print("Write to gdf")
    write_to_gdf(kps, str(image_file) + ".gdf")

    print("Write image with keypoints")
    annotated_image = image.copy()
    for i in range(len(kps)):
        kp = kps[i]
        pos = get_point_tuple(kp)
        cv2.putText(annotated_image, str(i) + ": " + str(int(kp.size)), pos, 1, 1, (0,0,255), 2, cv2.LINE_AA)
        
    write_image(annotated_image, "imgs/keypoints/" + str(image_file))




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
