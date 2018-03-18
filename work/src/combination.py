import os
#import random
import subprocess
import cv2
import numpy as np

import common.probability as cp
import common.matching as cm
import common.cv as cc
import common.write as cw

'''
from probability import *
from common_matching import *
from common_cv import get_image_kps, get_point_tuple, cv2window
'''

from typing import List, Tuple, Dict, Any
from classes.matching import LabelData, KeyLabel
from classes.graphs import Graph, Edge, Node

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
def bf_model(model: Any,
             matches: List[Tuple[KeyLabel, ...]],
             node_dis: Dict[str, LabelData],
             edge_dis: Dict[Edge, LabelData]) -> List[Tuple[KeyLabel, ...]]:

    # Get list of labels from model
    labels = [label for label,count in model.items() for i in range(count)]

    kp_list: List[Tuple[KeyLabel, ...]] = []
    for label in labels:
        prob_list: List[Tuple[KeyLabel, ...]] = []

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

            # Deal with overlap
            #for p in kp_list:

            kp_list = add_best_to_list(kp_list, s)

    return kp_list



def bf_graph(graph: Graph,
             matches: List[Tuple[KeyLabel, ...]],
             node_dis: Dict[str, LabelData],
             edge_dis: Dict[Edge, LabelData]) -> List[Tuple[KeyLabel, ...]]:

    kp_list: List[Tuple[KeyLabel, ...]] = []
    for edge in graph.edges:
        edge_tuple: Tuple[str, str] = (edge.n1.label, edge.n2.label)

        prob_list: List[Tuple[KeyLabel, ...]] = []
        for permutation in matches:
            triplet = [label.name for kp,label in permutation]
            for doublet in zip(triplet[:-1], triplet[1:]):
                if edge_tuple == doublet:
                    prob_list.append(permutation)

        if len(prob_list) > 0:
            s = sorted(prob_list, key=lambda kp_perm: cp.get_permutation_probability(node_dis, edge_dis, kp_perm), reverse=True)


            kp_list = add_best_to_list(kp_list, s)

    return kp_list


def add_best_to_list(kp_list: List[Tuple[KeyLabel, ...]],
                     sorted_prob: List[Tuple[KeyLabel, ...]]) -> List[Tuple[KeyLabel, ...]]:

    for new_permutation in sorted_prob:
            if not permutations_overlap(kp_list, new_permutation):
                return kp_list + [new_permutation]

    return kp_list
                            

def permutations_overlap(ps: List[Tuple[KeyLabel, ...]],
                         p2: Tuple[KeyLabel, ...]) -> bool:

    for p1 in ps:
        for kp1,label1 in p1:
            for kp2,label2 in p2:
                if kp1 == kp2 and label1 != label2:
                    return True
    return False
                    
            
def model_graph():
    body = Node(1, "body", 0)
    head = Node(2, "head", 0)
    claw1 = Node(3, "claw", 0)
    claw2 = Node(4, "claw", 0)
    arm1 = Node(5, "arm", 0)
    arm2 = Node(6, "arm", 0)
    back = Node(7, "back", 0)
    tail = Node(8, "tail", 0)

    nodes = [body, head, claw1, claw2,
             arm1, arm2, back, tail]

    edges = [
        Edge(body, back, 0),
        Edge(back, tail, 0),
        Edge(head, body, 0),
        Edge(claw1, arm1, 0),
        Edge(claw2, arm2, 0),
        Edge(arm1, body, 0),
        Edge(arm2, body, 0),
    ]

    return Graph(nodes, edges, 0.0)
    

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
    
    print("Writing graphs to file...")
    cw.permutations_as_query(permutations, permutation_size, "../queries/query")

    print("Start initial matching...")
    subprocess.run(["../ggsxe", "-f", "-gfu", "../new.gfu", "--multi", "../queries/query.querygfu"], stdout=FNULL)


    good_matches: List[Tuple[KeyLabel, ...]] = list(set(cm.get_matches(permutations, "graphs/complete/")))
    print("Get " + str(len(good_matches)) + " matches")

    
    '''
    for permutation_tuple in good_matches:
        kp, label = permutation_tuple[0]
        probability = cp.get_permutation_probability(node_distributions, edge_distributions, permutation_tuple)
    '''
        
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
    best_graph = bf_graph(model_graph(), good_matches, node_distributions, edge_distributions)


    print("kp: " + str(len(best_kp)))
    print("model:" + str(len(best_model)))
    print("graph:" + str(len(best_graph)))

    cw.write_triplets(best_kp, image_file, "imgs/method-kp/")
    cw.write_triplets(best_model, image_file, "imgs/method-model/")
    cw.write_triplets(best_graph, image_file, "imgs/method-graph/")
    cw.write_keypoints(image_file, kps)

    print("------------------------------")
