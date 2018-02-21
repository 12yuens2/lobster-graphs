import itertools
import subprocess
import os
import ast
from common_graph import *
#from common_cv import *


class Label():
    def __init__(self, name, size_min, size_max):
        self.name = name
        self.size_min = size_min
        self.size_max = size_max

    def __repr__(self):
        return str(self.name)


    def in_range(self, value):
        return self.size_min <= value <= self.size_max


def possible_node_labels(actual_size, labels):
    possible_labels = []
    for label in labels:
        label_name = label.name
        #target_size = label.size
        if label.in_range(actual_size):
            possible_labels.append(label_name)

    return possible_labels


def get_combinations(kps, label_params):
    kp_labels = []
    for kp in kps:
        labels = possible_node_labels(kp.size, label_params)
        if len(labels) > 0:
            kp_labels.append((kp,labels))

    combinations = []
    for kp,labels in kp_labels:
        combinations += list(itertools.product([kp],labels))

    return combinations

def get_permutations(combinations, length):
    permutations = list(itertools.permutations(combinations, length))

    # Filter out permutations where both keypoints are the same
    permutations = list(filter(lambda x: x[0][0] != x[1][0], permutations))
    return permutations



def write_as_query(permutations, filepath):
    for i in range(len(permutations)):
        permutation = permutations[i]
        f = open(filepath + str(i).zfill(4) + ".querygfu", "w")

        # Graph header
        f.write("#graph" + str(i) + "\n")

        f.write(str(len(permutation)) + "\n")

        for node in permutation:
            label = node[1]
            f.write(str(label) + "\n")

        f.write("2\n0 1\n1 2\n")
        f.flush()
        f.close()


def node_matches(query_graph, db_graph, matches):
    for query,target in matches:
        query_node = query_graph.get_node(query)
        target_node = db_graph.get_node(target)

        #print(str(query_node))
        #print(str(target_node))

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

            #if node_matches(query_graph, db_graph, matches):
                #good_matches.append(matches)
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
 
