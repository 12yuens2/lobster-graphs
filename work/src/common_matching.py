import itertools
import subprocess
import os
import ast

import common_graph as cg
import common_probability as cp


# Type imports
from typing import Dict, List, Any, Tuple
from cv2 import KeyPoint
from classes.matching import Label, LabelData, KeyLabel
from classes.graphs import Graph, Edge



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

            matches = list(ast.literal_eval(data[2][1:-1]))

            query_graph = cg.graph_from_permutation(permutations[query_id])
            db_graph = get_db_graph(db_id, db_path)

            if edge_matches(query_graph, db_graph, matches):
                good_matches.append(permutations[query_id])


    return good_matches
            
def get_db_graph(graph_id: int, graphs_path: str) -> Graph:
    with open(graphs_path+str(graph_id)+".gdf") as graph_file:
        lines = graph_file.read().splitlines()[1:]
        db_graph = cg.translate_graph(lines)

        # Offset node ids due to graph format translation issues
        for node in db_graph.nodes:
            node.node_id -= 1
        
        return db_graph

