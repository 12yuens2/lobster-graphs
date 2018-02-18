import itertools
import subprocess
import os
import ast
from translate import *
from probability import *
from sift_detection import * 

FNULL = open(os.devnull, "w")

class Node():
    def __init__(self, id, label):
        self.id = id
        self.label = label


    def __repr__(self):
        return str(str(self.id) + ": " + self.label)



class Label():
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return str(name)
    
def possible_node_labels(actual_size, labels):
    possible_labels = []
    for label in labels:
        label_name = label.name
        target_size = label.size
        if within_value(target_size, actual_size):
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

def write_as_query(permutations):
    for i in range(len(permutations)):
        permutation = permutations[i]
        f = open("../queries/query" + str(i) + ".querygfu", "w")

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
    return 0

def edge_matches(query_graph, db_graph):
    return 1

        
def get_matches(permutations):
    good_matches = []
    with open("matches", "r") as match_file:
        for line in match_file:
            data = line.strip().split(":")
            query_id = int(data[0])
            db_id = int(data[1])

            print(data[2])
            matches = list(ast.literal_eval(data[2][1:-1]))

            query_graph = graph_from_permutation(permutations[query_id])
            db_graph = get_db_graph(db_id)


            print("Query graph")
            print(query_graph)

            print("Database graph")
            print(db_graph)

            node_matches(query_graph, db_graph, matches)
            edge_matches(query_graph, db_graph, matches)

            return

    return good_matches
            
def get_db_graph(graph_id):
    path = "../graphs/"
    with open(path+str(graph_id)+".gdf") as graph_file:
        lines = graph_file.read().splitlines()[1:]
        return get_graph(lines)
        

label_params = [
    Label("body", 700),
    Label("arm", 200),
    Label("claw", 100),
    Label("head", 200),
    Label("tail", 320)
]

# 1. All node permutations

# 2. All node label combinations
kps = get_image_kps("imgs/dither/IMG_1380.JPG")


combinations = get_combinations(kps, label_params)
permutations = get_permutations(combinations,3)


print("Got " + str(len(kps)) + " keypoints.")
print(str(len(permutations)) + " permutations of size 3")

print("Writing graphs to file...")
write_as_query(permutations)


print("Start initial matching...")
subprocess.run(["../ggsxe", "-f", "-gfu", "../db.gfu", "--dir", "../queries/"], stdout=FNULL)
print("Finish initial matching...")


good_permutations = []
with open("matches", "r") as match_file:
    current_id = -1
    for line in match_file:
        graph_id = int(line.split(":")[0])

        if not graph_id == current_id:
            good_permutations.append(permutations[graph_id])
            current_id = graph_id

print(len(good_permutations))

get_matches(good_permutations)


