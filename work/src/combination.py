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
        f = open("../queries/query" + str(i) + ".querygfu", "w")

        # Graph header
        f.write("#graph" + str(i) + "\n")

        f.write(str(len(permutation)) + "\n")

        for node in permutation:
            label = node[1]
            f.write(label + "\n")

        f.write("2\n0 1\n1 2\n")
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

print("Got " + str(len(kps)) + " keypoints.")

combinations = get_combinations(kps, label_params)

print("Combinations:")
print(combinations)

permutations = get_permutations(combinations,3)

print("Permutations:")
print(str(len(permutations)))

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



def get_matches():
    with open("matches", "r") as match_file:
        for line in match_file:
            
