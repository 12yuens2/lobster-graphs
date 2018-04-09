import numpy as np

import common.cv as cc
import common.graph as cg
import common.probability as cp
import csv

from collections import Counter


# Annotated positions for precision/recall tests
def get_annotated_poses(image_file):
    annotated_nodes = get_annotated_nodes(image_file)
    annotated_poses = [node.pos for node in annotated_nodes]

    return annotated_poses


def get_annotated_nodes(image_file):
    annotated_file = open("graphs/annotated/" + image_file[4:8] + ".gdf")
    annotated_graph = cg.translate_graph(annotated_file.read().splitlines()[1:])

    return annotated_graph.nodes

def get_generated_poses(model):
    poses = []
    for tup in model:
        for keylabel in tup:
            kp,label = keylabel
            poses.append(cc.get_point_tuple(kp))

    return list(set(poses))

def get_label_positions(model, label):
    label_positions = []
    for tup in model:
        for keylabel in tup:
            kp,found_label = keylabel
            if found_label.name == label:
                label_positions.append(cc.get_point_tuple(kp))

    return list(set(label_positions))


def get_precision(annotated_poses, model_poses):
    tp = len(set(annotated_poses).intersection(model_poses))

    if len(model_poses) == 0:
        return 0
    
    return tp / len(model_poses)


def get_recall(annotated_poses, model_poses):
    tp = len(set(annotated_poses).intersection(model_poses))

    if len(annotated_poses) == 0 or tp == 0:
        return len(annotated_poses)
    
    return tp / len(annotated_poses)


def get_precision_recall(annotated_poses, model_poses):
    precision = get_precision(annotated_poses, model_poses)
    recall = get_recall(annotated_poses, model_poses)

    return (precision,recall)


def get_classification_metrics(annotated_poses, poses):
    tp = len(set(annotated_poses).intersection(poses))
    fp = len(poses)
    fn = len(annotated_poses)

    return (tp,fp,fn)

def update_dictionary(key, data, dictionary):
    if key in dictionary:
        total = dictionary[key]
        dictionary[key] = tuple(sum(x) for x in zip(total,data))
    else:
        dictionary[key] = data



def experiment_identification(image_file, method, model_category, best_model, experiment_dict):
    actual_category = "juvenile" if image_file[4] == "4" else "mature"
    annotated_poses = get_annotated_poses(image_file)
    poses = get_generated_poses(best_model)

    key = (method,model_category,actual_category)
    data = get_classification_metrics(annotated_poses, poses)
    update_dictionary(key, data, experiment_dict)
  

def experiment_label(image_file, method, model_category, label, best_model, experiment_dict):
    actual_category = "juvenile" if image_file[4] == "4" else "mature"
    annotated_nodes = get_annotated_nodes(image_file)
    filtered_nodes = [node.pos for node in annotated_nodes if node.label == label]
    poses = get_label_positions(best_model, label)

    key = (method,label,model_category,actual_category)
    data = get_classification_metrics(filtered_nodes, poses)
    update_dictionary(key, data, experiment_dict)

        
def write_experiment(csv_file, experiment_dict):
    writer = csv.writer(csv_file, delimiter=",")

    for key,data in experiment_dict.items():
        headers = list(key)
        tp,fp,fn = data

        precision = tp/fp # fp here is tp + fp
        recall = tp/fn # fn here is tp + fn

        writer.writerow(headers + [precision, recall])
        csv_file.flush()

def write_classify(csv_file, category_dict):
    writer = csv.writer(csv_file, delimiter=",")

    distances = []
    for image_file,classify_dict in category_dict.items():
        category = "juvenile" if image_file[4] == "4" else "mature"
        mg = classify_dict["graph","mature"]
        ml = classify_dict["model","mature"]
        jg = classify_dict["graph","juvenile"]
        jl = classify_dict["model","juvenile"]

        g_class = "mature" if mg > jg else "n" if mg == jg else "juvenile"
        l_class = "mature" if ml > jl else "n" if ml == jl else "juvenile"
        
        writer.writerow([image_file, category, mg, ml, jg, jl, g_class, l_class])
        csv_file.flush()

def classify(image_file, node_dis, edge_dis, category, method, model):
    psum = 0
    prod = 1
    for subgraph in model:
        probability = cp.get_permutation_probability(node_dis, edge_dis, subgraph)
        psum += probability
        prod *= np.exp(probability)

    print(image_file + " " + category + " " + method + " " + str(psum) + " " + str(prod))
        

def node_distance(nodes1, nodes2):
    distance = 0
    # Cost of deletion/insertion
    if len(nodes1) > len(nodes2):
        distance += len(nodes1) - len(nodes2)
    elif len(nodes2) > len(nodes1):
        distance += len(nodes2) - len(nodes1)

    # Cost of substitution
    c1 = Counter([node.label for node in nodes1])
    c2 = Counter([node.label for node in nodes2])
    diff = c2-c1
    print(list(diff.elements()))
    distance += len(list(diff.elements()))

    return distance

def edge_distance(edges1, edges2):
    distance = 0
    c1 = Counter([(e.n1.label, e.n2.label) for e in edges1])
    c2 = Counter([(e.n1.label, e.n2.label) for e in edges2])

    diff = c2-c1
    print(list(diff.elements()))

    return len(list(diff.elements())) + abs(len(edges1) - len(edges2))

# g1 is data graph
# g2 is model graph
def graph_distance(g1, g2):
    distance = 0
    distance += node_distance(g1.nodes, g2.nodes)
    distance += edge_distance(g1.edges, g2.edges)

    return distance

    
def experiment_classify(image_file, method, category, matched_subgraphs, model_graph, node_distribution, edge_distribution, category_dict):
    if not image_file in category_dict:
        category_dict[image_file] = {}

    psum = 0
    for subgraph in matched_subgraphs:
        for kp,label in subgraph:
            psum += label.probability

    # Multiplier determines balance of probability vs edit distance
    multiplier = 2
    matched_graph = cg.create_graph(matched_subgraphs)
    category_dict[image_file][method,category] = multiplier * psum / graph_distance(matched_graph, model_graph)
