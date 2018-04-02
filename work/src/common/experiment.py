import common.cv as cc
import common.graph as cg
import csv

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

        precision = tp/fp
        recall = tp/fn

        writer.writerow(headers + [precision, recall])
        csv_file.flush()
        
