#import itertools
import os
#import math
import numpy as np
import scipy.stats

'''
class PossibleGraph():
    def __init__(self, possible_nodes, edges):
        self.possible_nodes = possible_nodes
        self.edges = edges


    def permutations(self, edge_db):

        # Use itertools on possible_nodes to get all combinations of node labels
        permutations = list(itertools.product(*[possible_node.combinations() for possible_node in self.possible_nodes]))
        permutation_graphs = []

        for permutation in permutations:
            probability_assignment = 1
            for node in permutation:
                probability_assignment *= node.probability

            edges = self.get_new_edges(permutation)

            for edge in edges:
                if edge in edge_db:
                    probability_assignment *= edge_db[edge][edge.length]

            permutation_graphs.append(Graph(list(permutation), edges, probability_assignment))

        return permutation_graphs

    def get_new_edges(self, node_permutations):
        new_edges = []
        for edge in self.edges:
            node1 = 0
            node2 = 0
            for node in node_permutations:
                if node.node_id == edge.n1:
                    node1 = node

            for node in node_permutations:
                if node.node_id == edge.n2:
                    node2 = node

            new_edges.append(Edge(node1, node2, edge.length))

        return new_edges
            
            
# Node with probabilities
class PossibleNode():
    def __init__(self, node_id, labels):
        self.node_id = node_id
        self.labels = labels

    def combinations(self):
        return [Node(self.node_id, label, probability) for (label, probability) in self.labels.items()]



class Distribution():
    def __init__(self, label_tuple, data):
        self.label_tuple = label_tuple
        
        self.dictionary = {}
        self.populate_dictionary(data)
        
    def populate_dictionary(self, data):
        sum = 0
        for d in data:
            sum += 1

            if d in self.dictionary:
                self.dictionary[d] += 1
            else:
                self.dictionary[d] = 1

        for (k,v) in self.dictionary.items():
            self.dictionary[k] = v / sum

    def get_probability(self, item):
        if item in self.dictionary:
            return self.dictionary[item]
        else:
            return 1.0
'''


class LabelData():
    def __init__(self, label, distribution, probability):
        self.label = label
        self.distribution = distribution
        self.probability = probability

    def get_probability(self, value):
        return self.distribution.pdf(value) / self.probability

def load_node_data(filepath):
    label_data = {}

    for graph_file in os.listdir(filepath):
        f = open(filepath + graph_file)
        lines = f.readlines()[1:]
        for line in lines:
            if "edgedef>" in line:
                break

            l = line.split(",")
            label = l[1].strip("\"")
            size = float(l[2])

            if label in label_data:
                label_data[label].append(size)
            else:
                label_data[label] = [size]

    return label_data


def get_node_distributions(filepath):
    label_data = load_node_data(filepath)

    total_length = sum([len(data) for key,data in label_data.items()])
    
    for key,data in label_data.items():
        mean = np.mean(data)
        std = np.std(data)
        dis = scipy.stats.norm(mean, std)

        label_data[key] = LabelData(key, dis, len(data)/total_length)

    return label_data
    



def get_edge_distributions(filepath):
    graphs = []
    
    for graph_file in os.listdir(filepath):
        f = open(filepath + graph_file)
        lines = f.readlines()[1:]

        graphs.append(translate_graph(lines))

    for graph in graphs:
        for edge in graph.edges:
            
