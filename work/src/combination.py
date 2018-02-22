import os
import cv2
import numpy as np

from probability import *
from common_matching import *
from common_cv import get_image_kps, get_point_tuple, cv2window

FNULL = open(os.devnull, "w")
PATH = "imgs/dither/"
LABEL_THRESHOLD = 0.005

distributions = get_distributions("graphs/complete/")


'''
for label,data in distributions.items():
    print(str(label) + ": " + str(data.get_probability(100)))
label_params = [
    Label("body", 700),
    Label("arm", 200),
    Label("claw", 100),
    Label("head", 200),
    Label("tail", 320),
    Label("back", 200)
]
'''

# Remove old queries
#print("Removing old queries...")
#subprocess.run(["rm", "-f", "../queries/*"])
for image_file in os.listdir(PATH):
    print("Start " + image_file)
    kps = get_image_kps(PATH + image_file)

    combinations = get_combinations(kps, distributions, LABEL_THRESHOLD)
    permutations = get_permutations(combinations,3)


    print("Got " + str(len(kps)) + " keypoints.")
    print(str(len(permutations)) + " permutations of size 3")

    print("Writing graphs to file...")
    write_as_query(permutations, "../queries/query")


    print("Start initial matching...")
    subprocess.run(["../ggsxe", "-f", "-gfu", "../new.gfu", "--multi", "../queries/query.querygfu"], stdout=FNULL)

    good_matches = list(set(get_matches(permutations, "graphs/complete/")))

    print("Get " + str(len(good_matches)) + " matches")

    # draw lines and labels
    image = cv2.imread(PATH + image_file)
    y = 0
    for match in good_matches:
        for t1,t2 in zip(list(match)[:-1], list(match)[1:]):
            image = cv2.drawKeypoints(image, [t1[0], t2[0]], image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv2.line(image, get_point_tuple(t1[0]), get_point_tuple(t2[0]), (255,0,0), thickness=3)
            cv2.putText(image, str(t1[1]), tuple(map(sum, zip(get_point_tuple(t1[0]), (0,y)))), 1, 1, (0,0,255), 2, cv2.LINE_AA)
            y += 4
            cv2.putText(image, str(t2[1]), tuple(map(sum, zip(get_point_tuple(t2[0]), (0,y)))), 1, 1, (0,0,255), 2, cv2.LINE_AA)
            #print(str(t1) + " " + str(t2))
            y += 4

    #cv2window("test", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    cv2.imwrite("imgs/processed/" + image_file, image)
    print("-------------------------------")
