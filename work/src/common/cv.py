import cv2
import os
import math
import numpy as np

""" common_cv.py: All common functions that use OpenCV and deal with keypoints. """

HIST_BINS = [8,8,8]

### Metric functions ###

def get_distance(kp1, kp2):
    """ Return distance between 2 keypoints """
    pt1 = kp1.pt
    pt2 = kp2.pt
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

def get_point_tuple(kp):
    """ Get coordinates of keypoint as an int tuple """
    return (int(kp.pt[0]), int(kp.pt[1]))

def midpoint(kp1, kp2):
    """ Get midpoint between 2 keypoints """
    pt1 = get_point_tuple(kp1)
    pt2 = get_point_tuple(kp2)

    return (int((pt1[0] + pt2[0]) / 2), int((pt1[1] + pt2[1]) / 2)) 



### Keypoint descriptor functions ###

def closest_kp(keys, des, descriptor):
    """ Get a keypoints from keys that is closest to the given descriptor """
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
    """ Get the closest keypoint from the keypoint dictionary to a predefined descriptor """

    #Sort of keypoint size as body should be largest keypoint
    key_dict = sorted(key_dict.items(), key=lambda x: x[0].size, reverse=True)
    keys = [k for k,v in key_dict]
    des = [v for k,v in key_dict]

    body_descriptor = np.fromfile("body.kp", dtype=np.uint8)

    return closest_kp(keys[:3], des, body_descriptor)



### Filter Functions ###

def filter_keypoints_octave(kps):
    """ Filter keypoints by octave level """
    filtered_kps = []

    for kp in kps:
        octave = kp.octave & 0xFF #Fix for OpenCV SIFT octaves
        if 3 < octave < 8:
            filtered_kps.append(kp)

    return filtered_kps

def filter_keypoints_size(kps):
    """ Filter keypoints by size """
    filtered_kps = []

    for kp in kps:
        if kp.size > 80:
            filtered_kps.append(kp)

    return filtered_kps

def filter_keypoints_histogram(image, histogram, kps, method=cv2.HISTCMP_CORREL):
    """ Filter keypoints by colour histogram """
    filtered_kps = []

    for kp in kps:
        # Calculate histogram on BGR
        hist2 = cv2.calcHist([image], [0,1,2], mask_image(image, kp), HIST_BINS, [0,256,0,256,0,256])
        diff = cv2.compareHist(histogram, hist2, method)
        if diff > 0.5:
            filtered_kps.append(kp)

    return filtered_kps

def remove_duplicates(kps):
    """ Remove duplicate key points that have the same coordinates. """
    filtered_kps = []

    class KP():
        def __init__(self, kp, pos):
            self.kp = kp
            self.pos  = pos

        def __eq__(self, other):
            return self.pos == other.pos

        def __hash__(self):
            return hash(self.pos)


    KPs = []
    for kp in kps:
        (x,y) = get_point_tuple(kp)

        KPs.append(KP(kp, (x,y)))
       
    return list(a.kp for a in set(KPs)) #filtered_kps




### Functions to get keypoints from images ###
    
def get_all_keypoints(image_filename):
    """ Get all keypoints from a filename """
    sift = cv2.xfeatures2d.SIFT_create()
    image = cv2.imread(image_filename)

    # Detect keypoints
    sift_kps = sift.detect(image, None)
    sift_image = image.copy()
    keys, des = sift.compute(sift_image, sift_kps)
    keys_dict = dict(zip(keys, des))

    # Basic filter keypoints using octaves
    kps = filter_keypoints_octave(keys)

    return kps
    

def mask_image(image, keypoint):
    """ Return mask of an image of only the area of the keypoints """
    h,w = image.shape[:2]
    circle = np.zeros((h,w), np.uint8)

    # Get position and size of keypoint
    pos = get_point_tuple(keypoint)
    size = int(keypoint.size/2)    
    
    cv2.circle(circle, pos, size, 1, thickness=-1)
    return circle



def get_image_kps(image_file, hist_method=cv2.HISTCMP_CORREL):
    """ Get histogram filtered keypoints of an image """
    image = cv2.imread(image_file)
    kps = get_all_keypoints(image_file)

    # Load pre-defined histograms
    filtered_kps = []
    for hist_file in os.listdir("hists/"):
        hist = np.load("hists/" + hist_file)
        hist.reshape(8,8,8)

        filtered_kps += filter_keypoints_histogram(image, hist, kps, method=hist_method)

        #print(hist_file)
        #print(len(filtered_kps))

    return remove_duplicates([kp for kp in filtered_kps])



### Misc functions ###

def cv2window(window_name, image):
    """ Create a window and draw the image """
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, image)


def get_histogram(image, kp):
    return cv2.calcHist([image], [0,1,2], mask_image(image, kp), HIST_BINS, [0,256,0,256,0,256])

def drawKeypoints(image_file, keypoints):
    """ Draw all keypoints on given image """
    image = cv2.imread(image_file)
    return cv2.drawKeypoints(image, keypoints, image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

