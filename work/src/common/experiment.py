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

    if len(annotated_poses) == 0:
        return 0
    
    return tp / len(annotated_poses)


def get_precision_recall(annotated_poses, model_poses):
    precision = get_precision(annotated_poses, model_poses)
    recall = get_recall(annotated_poses, model_poses)

    return (precision,recall)


def experiment_file(image_file, model_category, best_model, best_graph, csv_file):
    writer = csv.writer(csv_file, delimiter=",")

    actual_category = "juvenile" if image_file[4] == "4" else "mature"

    annotated_poses = get_annotated_poses(image_file)
    model_poses = get_generated_poses(best_model)
    graph_poses = get_generated_poses(best_graph)

    model_precision, model_recall = get_precision_recall(annotated_poses, model_poses)
    graph_precision, graph_recall = get_precision_recall(annotated_poses, graph_poses)

    writer.writerow([image_file, "model", model_category, actual_category, model_precision, model_recall])
    writer.writerow([image_file, "graph", model_category, actual_category, graph_precision, graph_recall])

    csv_file.flush()



def experiment_label(image_file, method, model_category, label, best_model, experiment_dict):

    actual_category = "juvenile" if image_file[4] == "4" else "mature"
    annotated_nodes = get_annotated_nodes(image_file)
    filtered_nodes = [node.pos for node in annotated_nodes if node.label == label]
    poses = get_label_positions(best_model, label)

    pr = get_precision_recall(filtered_nodes, poses)

    #writer.writerow([image_file, method, model_category, actual_category, label, precision, recall])
    #csv_file.flush()

    if (method,label,model_category,actual_category) in experiment_dict:
        total = experiment_dict[method,label,model_category,actual_category]
        print(total)
        print(pr)
        print("-")
        experiment_dict[method,label,model_category,actual_category] = tuple(sum(x) for x in zip(total,pr))

        print(experiment_dict[method,label,model_category,actual_category])
        print("")
    else:
        experiment_dict[method,label,model_category,actual_category] = pr


        
def write_label_experiment(csv_file, experiment_dict):
    writer = csv.writer(csv_file, delimiter=",")

    for key,data in experiment_dict.items():
        method,label,model_category,actual_category = key
        precision,recall = data

        writer.writerow([method,model_category,actual_category,label,precision/20,recall/20])
        csv_file.flush()
        



