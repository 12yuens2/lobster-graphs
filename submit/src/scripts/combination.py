import os
import sys
import subprocess
import cv2
import numpy as np

import common.probability as cp
import common.matching as cm
import common.cv as cc
import common.write as cw
import common.graph as cg
import common.experiment as ce

from decimal import Decimal

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

def model_dict():
    return {"body": 1,
            "head": 1,
            "claw": 2,
            "arm":  2,
            "back": 1,
            "tail": 1 }


def remove_old_queries():
    print("Removing old queries...")
    for f in [f for f in os.listdir("../queries/")]:
        os.remove("../queries/" + f)

def get_unique_labels(subgraphs):
    labels = []
    for tup in subgraphs:
        for keylabel in tup:
            kp,label = keylabel
            labels.append(label.name)

    return list(set(labels))
    
PERMUTATION_SIZE = 3

# Thresholds from command line
LABEL_THRESHOLD = round(Decimal(float(sys.argv[1])),2)
HISTOGRAM_THRESHOLD = round(Decimal(float(sys.argv[2])),1)
IMAGE_PATH = "../../dataset/imgs/"

for image_file in os.listdir(IMAGE_PATH):
    
    for category in ["juvenile", "mature"]:

        print("Running pipeline on " + category + " model.")

        # Get probability distributions from annotated dataset
        node_distributions = cp.get_node_distributions("graphs/complete/" + category + "/")
        edge_distributions = cp.get_edge_distributions("graphs/complete/" + category + "/") 

        print("Start " + image_file)
        kps = cc.get_image_kps(cw.PATH + image_file, HISTOGRAM_THRESHOLD)

        # Remove old queries
        remove_old_queries() 

        # Get labelling combinations
        combinations = cm.get_combinations(kps, node_distributions, LABEL_THRESHOLD)

        # Get subgraph permutations
        permutations = cm.get_permutations(combinations, PERMUTATION_SIZE)

        print("Got " + str(len(kps)) + " keypoints.")
        print(str(len(permutations)) + " permutations of size " + str(PERMUTATION_SIZE))

        #print("Writing graphs to file...")
        cw.permutations_as_query(permutations, PERMUTATION_SIZE, "/tmp/query")

        matches = cm.run_matching(category, permutations)

        # Do different methods to get triplets
        best_kp = cm.bf_keypoints(kps, matches, node_distributions, edge_distributions)
        best_model = cm.bf_model(model_dict(), matches, node_distributions, edge_distributions)
        best_graph = cm.bf_graph(model_graph(), matches, node_distributions, edge_distributions)

        # Write images with keypoints drawn
        #cw.write_triplets(best_kp, image_file, "imgs/test/kp")
        #cw.write_triplets(best_model, image_file, "imgs/test/label")
        #cw.write_triplets(best_graph, image_file, "imgs/test/graph")
        #cw.write_keypoints(image_file, kps)

        # Gather data for experiments if needed after all steps

        print("------------------------------")