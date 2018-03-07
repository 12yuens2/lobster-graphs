import os
import random
import cv2
import numpy as np

from probability import *
from common_matching import *
from common_cv import get_image_kps, get_point_tuple, cv2window

FNULL = open(os.devnull, "w")
PATH = "imgs/dither/"
LABEL_THRESHOLD = 0.00025

node_distributions = get_node_distributions("graphs/complete/")


edge_distributions = get_edge_distributions("graphs/complete/")

# Remove old queries
#print("Removing old queries...")
#subprocess.run(["rm", "-f", "../queries/*"])
           

# Brute force - get best triplet for each key point
def bf_keypoints(kps, matches, node_dis, edge_dis):
    kp_list = []
    for kp in kps:
        prob_list = []

        # Get all permutations for each keypoint
        for permutation in matches:
            for x in permutation:
                if kp in x:
                    prob_list.append(permutation)

        # Sort by probability and add best permutation to list
        if len(prob_list) > 0:
            s = sorted(prob_list, key=lambda kp_perm: get_permutation_probability(node_dis, edge_dis, kp_perm), reverse=True)

            kp_list += s[:1]

    return kp_list

# Brute force - best triplet for each label in ideal model
def bf_model(model, matches, node_dis, edge_dis):

    # Get list of labels from model
    labels = [label for label,count in model.items() for i in range(count)]

    kp_list = []
    for label in labels:
        prob_list = []

        # Get all permutations that contain the label
        for permutation in matches:
            prob_list += [permutation for x in permutation if label == x[1].name]
            '''
            for x in permutation:
                if label == x[1].name:
                    prob_list.append(permutation)
            '''

        # Get best permutation that contains label
        if len(prob_list) > 0:
            s = sorted(prob_list, key=lambda kp_perm: get_permutation_probability(node_dis, edge_dis, kp_perm), reverse=True)

            #for p in kp_list:
                

            kp_list += s[:1]

    return kp_list


def write_triplets(triplets, image_file, write_path):
    image = cv2.imread(PATH + image_file)
    
    for triplet in triplets:
        for n1,n2 in zip(list(triplet)[:-1], list(triplet)[1:]):
            image = cv2.drawKeypoints(image, [n1[0], n2[0]], image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            cv2.line(image, get_point_tuple(n1[0]), get_point_tuple(n2[0]), (255,0,0), thickness=3)
            cv2.putText(image, str(n1[1]), get_point_tuple(n1[0]), 1, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(image, str(n2[1]), get_point_tuple(n2[0]), 1, 1, (0,0,255), 2, cv2.LINE_AA)

    cv2.imwrite(write_path + image_file, image)


def write_keypoints(image_file, kps):
    image = cv2.imread(PATH + image_file)
    cv2.drawKeypoints(image, kps, image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite("imgs/keypoints/" + image_file, image)

    

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
    combinations = get_combinations(kps, node_distributions, LABEL_THRESHOLD)
    permutations = get_permutations(combinations, permutation_size)


    print("Got " + str(len(kps)) + " keypoints.")
    print(str(len(permutations)) + " permutations of size " + str(permutation_size))

    print(permutations[0])

    
    print("Writing graphs to file...")
    write_as_query(permutations, permutation_size, "../queries/query")

    print("Start initial matching...")
    subprocess.run(["../ggsxe", "-f", "-gfu", "../new.gfu", "--multi", "../queries/query.querygfu"], stdout=FNULL)

    good_matches = list(set(get_matches(permutations, "graphs/complete/")))
    print("Get " + str(len(good_matches)) + " matches")


    print(good_matches[0])
    
    for permutation_tuple in good_matches:
        kp, label = permutation_tuple[0]
        probability = get_permutation_probability(node_distributions, edge_distributions, permutation_tuple)
        
    print(good_matches[0])

    #1. Take 1 random match
    #2. Check against model and existing subgraph labels
    #3. Keep taking another random match until no more matches or model is filled, do not take match if label/keypoint already exists
    #4. Put all matches together as one graph and give probability as sum?product? of all matches
    #5. Do not have to worry about duplicate labels/keypoints because we can connect them all together rather than connect the exact matched subgraphs

    '''
    models = []
    for i in range(10):
        current_model = Model(model.copy())

        r = list(random.choice(good_matches))
        current_model.add_if_valid(r)
    '''

    '''
    current_model = Model(model.copy())
    for triplet in kp_list:
        current_model.add_if_valid(triplet)

    print(current_model.labels)
    '''


    best_kp = bf_keypoints(kps, good_matches, node_distributions, edge_distributions)
    best_model = bf_model(model, good_matches, node_distributions, edge_distributions)
    

    write_triplets(best_kp, image_file, "imgs/kp-method/")
    write_triplets(best_model, image_file, "imgs/model-method/")
    write_keypoints(image_file, kps)

    print("------------------------------")
