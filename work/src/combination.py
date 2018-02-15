import itertools
import subprocess
import os
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

def write_as_query(permutation):
    f = open("../queries/query0.querygfu", "w")

    # Graph header
    f.write("#graph0\n")

    f.write(str(len(permutation)) + "\n")

    for node in permutation:
        label = node[1]
        f.write(label + "\n")

    f.write("2\n")
    f.write("0 1\n")
    f.write("1 2\n")

    f.flush()
    f.close()
    


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

print("Combinations:")
print(combinations)

permutations = get_permutations(combinations,3)

print("Permutations:")
print(str(len(permutations)))

possible_permutations = []
for permutation in permutations:
    # Write permutation to graph format to query db
    write_as_query(permutation)

    # Query db
    process = subprocess.run(["../ggsxe", "-f", "-gfu", "../db.gfu", "--dir", "../queries/"], stdout=FNULL)

    # Check output from query
    matches = os.stat("matches").st_size
    if matches > 0:
        print("Add possible permutation: " + str(permutation))
        possible_permutations.append(permutation)

print(len(possible_permutations))


'''
nodes = []
for lc in label_combinations:
    nodes.append(Node(lc[0], lc[1]))

print(str(nodes[1].id) + ": " + nodes[1].label)

permutations = list(itertools.permutations(nodes, 3))
filtered = list(filter(lambda x: x[0].id != x[1].id, permutations))

print(len(permutations))
print(len(filtered))
'''

