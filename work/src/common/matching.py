import itertools
import subprocess
import os
import ast

import common.graph as cg
import common.probability as cp


# Type imports
from typing import Dict, List, Any, Tuple
from cv2 import KeyPoint
from classes.matching import Label, LabelData, KeyLabel
from classes.graphs import Graph, Edge


FNULL = open(os.devnull, "w")

'''
class Node():
    def __init__(self, kp, label):
        print(type(kp))
        self.kp = kp
        self.label = label
'''
    

'''
class Permutation():
    def __init__(self, tuple: KeyLabel, probability: float) -> None:
        self.tuple: KeyLabel = tuple
        self.probability: float = probability
'''
   
def possible_node_labels(actual_size: float,
                         label_distributions: Dict[str, LabelData],
                         label_threshold: float) -> List[Label]:

    possible_labels = []

    for label,label_data in label_distributions.items():
        probability = label_data.get_probability(actual_size)
        if probability > label_threshold:
            possible_labels.append(Label(label, probability))

    return possible_labels


def get_combinations(kps: List[Any],
                     label_distributions: Dict[str, LabelData],
                     label_threshold: float) -> List[KeyLabel]:
    kp_labels = []
    for kp in kps:
        labels = possible_node_labels(kp.size, label_distributions, label_threshold)
        if len(labels) > 0:
            kp_labels.append((kp,labels))

    combinations: List[Tuple[KeyPoint, Label]] = []
    for kp,labels in kp_labels:
        combinations += list(itertools.product([kp],labels))

    return combinations


def get_permutations(combinations: List[KeyLabel],
                     length: int) -> List[Tuple[KeyLabel, ...]]:

    permutation_tuples = list(itertools.permutations(combinations, length))
                 
    # Filter out permutations where both keypoints are the same
    permutation_tuples = list(filter(lambda x: x[0][0] != x[1][0], permutation_tuples))

    return permutation_tuples




'''
def node_matches(query_graph, db_graph, matches):
    for query,target in matches:
        query_node = query_graph.get_node(query)
        target_node = db_graph.get_node(target)

        if query_node != target_node:
            return False

    return True
'''

def edge_matches(query_graph: Graph,
                 db_graph: Graph,
                 matches: List[Tuple[int, int]]) -> bool:

    for t1,t2 in zip(matches[:-1], matches[1:]):
        query_edge: Edge = query_graph.get_edge(t1[0], t2[0])
        target_edge: Edge = db_graph.get_edge(t1[1], t2[1])

        if query_edge != target_edge:
            return False

    return True

        
def get_matches(permutations: List[Tuple[KeyLabel, ...]],
                db_path: str) -> List[Tuple[KeyLabel, ...]]:
    good_matches = []
    with open("matches", "r") as match_file:
        for line in match_file:
            data = line.strip().split(":")
            query_id = int(data[0])
            db_id = int(data[1])
            permutation = permutations[query_id]

            matches = list(ast.literal_eval(data[2][1:-1]))

            query_graph = cg.graph_from_permutation(permutation)
            db_graph = get_db_graph(db_id, db_path)

            if edge_matches(query_graph, db_graph, matches):
                good_matches.append(permutation)


    return good_matches
            
def get_db_graph(graph_id: int, graphs_path: str) -> Graph:
    with open(graphs_path+str(graph_id)+".gdf") as graph_file:
        lines = graph_file.read().splitlines()[1:]
        db_graph = cg.translate_graph(lines)

        # Offset node ids due to graph format translation issues
        for node in db_graph.nodes:
            node.node_id -= 1
        
        return db_graph



def run_matching(category: str,
                 permutations: List[Tuple[KeyLabel, ...]]) -> List[Tuple[KeyLabel, ...]]:

    # Match with graphgrep
    print("Start initial matching...")
    subprocess.run(["../ggsxe", "-f", "-gfu", "../" + category + ".gfu", "--multi", "../queries/query.querygfu"], stdout=FNULL)
    print("Finish matching")

    # Get good matches from graphgrep output
    good_matches: List[Tuple[KeyLabel, ...]] = list(set(get_matches(permutations, "graphs/complete/" + category + "/")))
    print("Get " + str(len(good_matches)) + " matches")

    return good_matches


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

