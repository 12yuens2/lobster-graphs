import os
#import random
import subprocess
import cv2
import numpy as np

import common_probability as cp
import common_matching as cm
import common_cv as cc
import common_write as cw

'''
from probability import *
from common_matching import *
from common_cv import get_image_kps, get_point_tuple, cv2window
'''

FNULL = open(os.devnull, "w")
LABEL_THRESHOLD = 0.00025

node_distributions = cp.get_node_distributions("graphs/complete/")


edge_distributions = cp.get_edge_distributions("graphs/complete/")

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
            s = sorted(prob_list, key=lambda kp_perm: cp.get_permutation_probability(node_dis, edge_dis, kp_perm), reverse=True)

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
            s = sorted(prob_list, key=lambda kp_perm: cp.get_permutation_probability(node_dis, edge_dis, kp_perm), reverse=True)

            #for p in kp_list:
                

            kp_list += s[:1]

    return kp_list

    

# Model of lobster to match to
model = {"body": 1,
         "head": 1,
         "claw": 2,
         "arm": 2,
         "back": 1,
         "tail": 1}

for image_file in os.listdir(cw.PATH):
    print("Start " + image_file)
    kps = cc.get_image_kps(cw.PATH + image_file)

    permutation_size = 3
    combinations = cm.get_combinations(kps, node_distributions, LABEL_THRESHOLD)
    permutations = cm.get_permutations(combinations, permutation_size)


    print("Got " + str(len(kps)) + " keypoints.")
    print(str(len(permutations)) + " permutations of size " + str(permutation_size))

    print(permutations[0])

    
    print("Writing graphs to file...")
    cw.permutations_as_query(permutations, permutation_size, "../queries/query")

    print("Start initial matching...")
    subprocess.run(["../ggsxe", "-f", "-gfu", "../new.gfu", "--multi", "../queries/query.querygfu"], stdout=FNULL)

    good_matches = list(set(cm.get_matches(permutations, "graphs/complete/")))
    print("Get " + str(len(good_matches)) + " matches")


    print(good_matches[0])
    
    for permutation_tuple in good_matches:
        kp, label = permutation_tuple[0]
        probability = cp.get_permutation_probability(node_distributions, edge_distributions, permutation_tuple)
        
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
    

    cw.write_triplets(best_kp, image_file, "imgs/kp-method/")
    cw.write_triplets(best_model, image_file, "imgs/model-method/")
    cw.write_keypoints(image_file, kps)

    print("------------------------------")
