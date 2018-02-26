#import itertools
import os
#import math
import numpy as np
import scipy.stats
from common_graph import translate_graph


class LabelData():
    def __init__(self, label, distribution, probability):
        self.label = label
        self.distribution = distribution
        self.probability = probability

    def get_probability(self, value):
        return self.distribution.pdf(value) * self.probability

def load_node_data(filepath):
    node_dict = {}

    for graph_file in os.listdir(filepath):
        f = open(filepath + graph_file)
        lines = f.readlines()[1:]
        for line in lines:
            if "edgedef>" in line:
                break

            l = line.split(",")
            label = l[1].strip("\"")
            size = float(l[2])

            if label in node_dict:
                node_dict[label].append(size)
            else:
                node_dict[label] = [size]

    return node_dict

def load_edge_data(filepath):
    edge_dict = {}
    
    for graph_file in os.listdir(filepath):
        f = open(filepath + graph_file)
        lines = f.readlines()[1:]

        graph = translate_graph(lines)

        for edge in graph.edges:
            length = edge.length
            edge.length = 0

            if edge in edge_dict:
                edge_dict[edge].append(length)
            else:
                edge_dict[edge] = [length]

    return edge_dict   


def get_distribution(data_dict):
    total_length = sum([len(data) for key,data in data_dict.items()])

    for key,data in data_dict.items():
       mean = np.mean(data)
       std = np.std(data)
       dis = scipy.stats.norm(mean, std)

       data_dict[key] = LabelData(key, dis, len(data)/total_length)

    return data_dict

def get_node_distributions(filepath):
    node_dict = load_node_data(filepath)

    return get_distribution(node_dict)

    '''

    total_length = sum([len(data) for key,data in node_dict.items()])
    
    for key,data in node_dict.items():
        mean = np.mean(data)
        std = np.std(data)
        dis = scipy.stats.norm(mean, std)

        node_dict[key] = LabelData(key, dis, len(data)/total_length)

    return node_dict
    '''

def get_edge_distributions(filepath):
    edge_dict = load_edge_data(filepath)

    return get_distribution(edge_dict)


def get_permutation_probability(permutation_tuple):
    return 0
