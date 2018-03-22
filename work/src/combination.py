import os
import sys
import subprocess
import cv2
import numpy as np

import common.probability as cp
import common.matching as cm
import common.cv as cc
import common.write as cw


from typing import List, Tuple, Dict, Any
from classes.matching import LabelData, KeyLabel
from classes.graphs import Graph, Edge, Node


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
    

FNULL = open(os.devnull, "w")
LABEL_THRESHOLD = 0.00025

category = sys.argv[1]

if not (category == "juvenile" or category == "mature"):
    print("Category " + category + " not recognised!")
    exit(1)


print("Running pipeline on " + category + " model.")
node_distributions = cp.get_node_distributions("graphs/complete/" + category + "/")
edge_distributions = cp.get_edge_distributions("graphs/complete/" + category + "/")

for image_file in os.listdir(cw.PATH):
    print("Start " + image_file)
    kps = cc.get_image_kps(cw.PATH + image_file)

    # Remove old queries
    print("Removing old queries...")
    for f in [f for f in os.listdir("../queries/")]:
        os.remove("../queries/" + f) 

        
    permutation_size = 3
    combinations = cm.get_combinations(kps, node_distributions, LABEL_THRESHOLD)
    permutations = cm.get_permutations(combinations, permutation_size)

    print("Got " + str(len(kps)) + " keypoints.")
    print(str(len(permutations)) + " permutations of size " + str(permutation_size))
    
    print("Writing graphs to file...")
    cw.permutations_as_query(permutations, permutation_size, "../queries/query")

   
    #1. Take 1 random match
    #2. Check against model and existing subgraph labels
    #3. Keep taking another random match until no more matches or model is filled, do not take match if label/keypoint already exists
    #4. Put all matches together as one graph and give probability as sum?product? of all matches
    #5. Do not have to worry about duplicate labels/keypoints because we can connect them all together rather than connect the exact matched subgraphs
    
    matches = run_matching("../" + category + ".gfu", permutations)
    
    # Do different methods to get triplets
    best_kp = bf_keypoints(kps, matches, node_distributions, edge_distributions)
    best_model = bf_model(model, matches, node_distributions, edge_distributions)
    best_graph = bf_graph(model_graph(), matches, node_distributions, edge_distributions)


    print("kp: " + str(len(best_kp)))
    print("model:" + str(len(best_model)))
    print("graph:" + str(len(best_graph)))

    cw.write_triplets(best_kp, image_file, "imgs/method-kp/" + category + "/")
    cw.write_triplets(best_model, image_file, "imgs/method-model/" + category + "/")
    cw.write_triplets(best_graph, image_file, "imgs/method-graph/" + category + "/")
    cw.write_keypoints(image_file, kps)

    print("------------------------------")
