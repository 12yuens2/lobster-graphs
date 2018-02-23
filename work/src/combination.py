import os
import random
import cv2
import numpy as np

from probability import *
from common_matching import *
from common_cv import get_image_kps, get_point_tuple, cv2window

FNULL = open(os.devnull, "w")
PATH = "imgs/dither/"
LABEL_THRESHOLD = 0.005

distributions = get_node_distributions("graphs/complete/")


# Remove old queries
#print("Removing old queries...")
#subprocess.run(["rm", "-f", "../queries/*"])




class Model():
    def __init__(self, labels):
        self.labels = labels.copy()
        self.current_nodes = []

    def __repr__(self):
        return str(self.labels) + "\n" + str(self.current_nodes)
        
    def check_nodes(self, nodes):
        for kp,label in nodes:
            if kp in [t[0] for t in self.current_nodes]:
                return False
            #elif label.name in self.labels and self.labels[label.name] <= 0:
                # bug if count is 1 but two instances of that label in nodes
                #return False
        return True

    def add_nodes(self, nodes):
        self.current_nodes += nodes
        for kp,label in nodes:
            self.labels[label.name] -= 1

    def add_if_valid(self, nodes):
        if self.check_nodes(nodes):
            self.add_nodes(nodes)
            

# Model of lobster to match to
model = {"body": 1,
         "head": 1,
         "claw": 2,
         "arm": 2,
         "back": 1,
         "tail": 1}

for image_file in os.listdir(PATH):
    print("Start " + image_file)
    kps = get_image_kps(PATH + image_file)

    permutation_size = 3
    combinations = get_combinations(kps, distributions, LABEL_THRESHOLD)
    permutations = get_permutations(combinations, permutation_size)


    print("Got " + str(len(kps)) + " keypoints.")
    print(str(len(permutations)) + " permutations of size " + str(permutation_size))

    print("Writing graphs to file...")
    write_as_query(permutations, "../queries/query")

    print("Start initial matching...")
    subprocess.run(["../ggsxe", "-f", "-gfu", "../new.gfu", "--multi", "../queries/query.querygfu"], stdout=FNULL)

    good_matches = list(set(get_matches(permutations, "graphs/complete/")))
    print("Get " + str(len(good_matches)) + " matches")


    #1. Take 1 random match
    #2. Check against model and existing subgraph labels
    #3. Keep taking another random match until no more matches or model is filled, do not take match if label/keypoint already exists
    #4. Put all matches together as one graph and give probability as sum?product? of all matches
    #5. Do not have to worry about duplicate labels/keypoints because we can connect them all together rather than connect the exact matched subgraphs

    models = []
    for i in range(10):
        current_model = Model(model.copy())

        r = list(random.choice(good_matches))
        current_model.add_if_valid(r)


        for i in range(54):
            r = list(random.choice(good_matches))
            current_model.add_if_valid(r)

        models.append(current_model)

    
    s = sorted(models, key=lambda model: sum([label.probability for kp,label in model.current_nodes]), reverse=True)

    # draw lines and labels
    image = cv2.imread(PATH + image_file)
    '''
    y = 0
    for match in s[:5]:
        for t1,t2 in zip(list(match)[:-1], list(match)[1:]):
            image = cv2.drawKeypoints(image, [t1[0], t2[0]], image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            cv2.line(image, get_point_tuple(t1[0]), get_point_tuple(t2[0]), (255,0,0), thickness=3)

            cv2.putText(image, str(t1[1].name), tuple(map(sum, zip(get_point_tuple(t1[0]), (0,y)))), 1, 1, (0,0,255), 2, cv2.LINE_AA)
            y += 4
            cv2.putText(image, str(t2[1].name), tuple(map(sum, zip(get_point_tuple(t2[0]), (0,y)))), 1, 1, (0,0,255), 2, cv2.LINE_AA)
            y += 4

    #cv2window("test", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    '''

    i = 1
    for match in s[:5]:
        image = cv2.imread(PATH + image_file)
        for n1,n2 in zip(match.current_nodes[:-1], match.current_nodes[1:]):
            image = cv2.drawKeypoints(image, [n1[0], n2[0]], image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            cv2.line(image, get_point_tuple(n1[0]), get_point_tuple(n2[0]), (255,0,0), thickness=3)
            cv2.putText(image, str(n1[1]), get_point_tuple(n1[0]), 1, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(image, str(n2[1]), get_point_tuple(n2[0]), 1, 1, (0,0,255), 2, cv2.LINE_AA)
    

        cv2.imwrite("imgs/processed/" + image_file + str(i) + ".jpg", image)
        i += 1
    print("-------------------------------")
