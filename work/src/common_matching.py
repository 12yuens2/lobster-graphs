import itertools
import subprocess
import os
import ast
from common_graph import *
from probability import get_permutation_probability
#from common_cv import *



# Type imports
from typing import Dict, List, Any, Tuple
from cv2 import KeyPoint
from probability import LabelData


class Model():
    def __init__(self, labels):
        self.labels = labels.copy()
        self.triplets = []

    def __repr__(self):
        return str(self.labels) + "\n" + str(self.triplet)
        
    def check_nodes(self, nodes):
        for kp,label in nodes:
            if kp in [t[0] for t in self.triplets]:
                return False
            #elif label.name in self.labels and self.labels[label.name] <= 0:
                # bug if count is 1 but two instances of that label in nodes
                #return False
        return True

    def add_nodes(self, nodes):
        self.triplets += nodes

        for kp,label in nodes:
            self.labels[label.name] -= 1

    def add_if_valid(self, nodes):
        if self.check_nodes(nodes):
            self.add_nodes(nodes)

 

class Label():
    def __init__(self, name: str, probability: float) -> None:
        self.name: str = name
        self.probability: float = probability


    def __repr__(self):
        return str(self.name) + ": " + str(self.probability)


'''
class Node():
    def __init__(self, kp, label):
        print(type(kp))
        self.kp = kp
        self.label = label
'''
    
class Permutation():
    def __init__(self, tuple, probability):
        self.tuple = tuple
        self.probability = probability

   
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
                     label_threshold: float) -> List[Tuple[KeyPoint, Label]]:
    kp_labels = []
    for kp in kps:
        labels = possible_node_labels(kp.size, label_distributions, label_threshold)
        if len(labels) > 0:
            kp_labels.append((kp,labels))

    combinations: List[Tuple[KeyPoint, Label]] = []
    for kp,labels in kp_labels:
        combinations += list(itertools.product([kp],labels))

    return combinations

def get_permutations(combinations, length):
    permutation_tuples = list(itertools.permutations(combinations, length))
                 
    # Filter out permutations where both keypoints are the same
    permutation_tuples = list(filter(lambda x: x[0][0] != x[1][0], permutation_tuples))

    return permutation_tuples



def write_as_query(permutations, permutation_size, filepath):
    f = open(filepath + ".querygfu", "w")
    for i in range(len(permutations)):
        permutation = permutations[i]

        # Graph header
        f.write("#graph" + str(i) + "\n")

        f.write(str(permutation_size) + "\n")

        for node in permutation:
            label = node[1].name
            f.write(str(label) + "\n")

        f.write("2\n0 1\n1 2\n")
        f.flush()
    f.close()


def node_matches(query_graph, db_graph, matches):
    for query,target in matches:
        query_node = query_graph.get_node(query)
        target_node = db_graph.get_node(target)

        if query_node != target_node:
            return False

    return True

def edge_matches(query_graph, db_graph, matches):
    for t1,t2 in zip(matches[:-1], matches[1:]):
        query_edge = query_graph.get_edge(t1[0], t2[0])
        target_edge = db_graph.get_edge(t1[1], t2[1])

        if query_edge != target_edge:
            return False

    return True

        
def get_matches(permutations, db_path):
    good_matches = []
    with open("matches", "r") as match_file:
        for line in match_file:
            data = line.strip().split(":")
            query_id = int(data[0])
            db_id = int(data[1])

            matches = list(ast.literal_eval(data[2][1:-1]))

            query_graph = graph_from_permutation(permutations[query_id])
            db_graph = get_db_graph(db_id, db_path)

            if edge_matches(query_graph, db_graph, matches):
                good_matches.append(permutations[query_id])


    return good_matches
            
def get_db_graph(graph_id, graphs_path):
    with open(graphs_path+str(graph_id)+".gdf") as graph_file:
        lines = graph_file.read().splitlines()[1:]
        db_graph = translate_graph(lines)

        # Offset node ids due to graph format translation issues
        for node in db_graph.nodes:
            node.node_id -= 1
        
        return db_graph
 
