import itertools
import os
#import math
import numpy as np
import scipy.stats

from common.graph import translate_graph, graph_from_permutation


# Type imports
from typing import Dict, List
from classes.graphs import Node, Edge
from classes.matching import DictKey, LabelData


def load_node_data(filepath: str) -> Dict[str, List[int]]:
    node_dict: Dict[str, List[int]] = {}

    for graph_file in os.listdir(filepath):
        f = open(filepath + graph_file)
        lines = f.readlines()[1:]
        for line in lines:
            if "edgedef>" in line:
                break

            l = line.split(",")
            label = l[1].strip("\"")
            size = int(float(l[2]))

            if label in node_dict:
                node_dict[label].append(size)
            else:
                node_dict[label] = [size]

    return node_dict

def load_edge_data(filepath: str) -> Dict[Edge, List[int]]:
    edge_dict: Dict[Edge, List[int]] = {}
    
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


def get_distribution(data_dict: Dict[DictKey, List[int]]) -> Dict[DictKey, LabelData]:
    total_length = sum([len(data) for key,data in data_dict.items()])

    sizes = [size for key,data in data_dict.items() for size in data]
    mean_size = np.mean(sizes)
    std_size = np.std(sizes)
    size_dis = scipy.stats.norm(mean_size, std_size)
    
    distribution = {}
    for key,data in data_dict.items():
       mean = np.mean(data)
       std = np.std(data)
       dis = scipy.stats.norm(mean, std)

       distribution[key] = LabelData(key, dis, size_dis, len(data)/total_length)

    return distribution

def get_node_distributions(filepath: str) -> Dict[str, LabelData]:
    node_dict: Dict[str, List[int]] = load_node_data(filepath)

    return get_distribution(node_dict)

def get_edge_distributions(filepath: str) -> Dict[Edge, LabelData]:
    edge_dict: Dict[Edge, List[int]] = load_edge_data(filepath)

    return get_distribution(edge_dict)


def get_permutation_probability(node_distributions, edge_distributions, permutation_tuple):

    total_probability = 0
    
    # Create triplet graph from permutation
    triplet = graph_from_permutation(permutation_tuple)
   
    for kp,label in permutation_tuple:
        total_probability += np.log(label.probability)

    for edge in triplet.edges:
        length = edge.length
        edge.length = 0

        if edge in edge_distributions:
            edge_label_data = edge_distributions[edge]
            edge_probability = edge_label_data.get_probability(length)

            if edge_probability > 0:
                total_probability += np.log(edge_probability)
            else:
                return 0
        else:
            return 0

    return total_probability
