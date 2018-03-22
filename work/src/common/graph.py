#import itertools
import math
import common.cv as cc

# Type imports
from typing import Dict, List, Tuple, Any, Optional
from cv2 import KeyPoint

from classes.graphs import Graph, Edge, Node
from classes.matching import KeyLabel


def within_value(v1, v2):
    """ Check if actual_value is within 10% of target value """
    percentage = 0.1
    error_allowed = percentage * v1
    high = v1 + error_allowed
    low = v1 - error_allowed

    return low <= v2 <= high


def graph_from_permutation(permutation: Tuple[KeyLabel,...]) -> Graph:
    """ Take permutation of n (keypoint, label) tuples and turn into a graph object """
    nodes = []
    for i in range(len(permutation)):
        nodes.append(Node(i, permutation[i][1].name, permutation[i][0].size, kp=permutation[i][0]))

    edges = []
    for n1,n2 in zip(nodes[:-1], nodes[1:]):
        edges.append(Edge(n1, n2, cc.get_distance(n1.kp, n2.kp)))

    return Graph(nodes, edges, 0)


def distance(pt1, pt2):
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

def translate_graph(lines: List[str]) -> Graph:
    """ Translate graph from gdf to graphgrep query format """
    nodes = []
    edges = []
    is_node = True

    # first_value used to offset node/edge ids to start from 0
    first = True
    first_value = 0

    for line in lines:
        a = line.split(",")

        if "edge" in line:
            is_node = False
        elif is_node:
            if first:
                first = False
                first_value = int(a[0])

            # Create node with Node(id, label, size)
            pos_x = float(a[4])
            pos_y = float(a[5])
            n = Node(int(a[0]),
                     str(a[1]).replace("\"", ""),
                     int(float(a[2])),
                     kp=KeyPoint(pos_x, pos_y, float(a[2])),
                     pos=(float(a[4]),float(a[5])))

            if (a[1] == ""):
                print("Node " + a[0] + " missing label.")
                exit(1)
            nodes.append(n)
        else:
            n1 = None
            n2 = None
            for node in nodes:
                if node.node_id == int(a[0]):
                    n1 = node
            for node in nodes:
                if node.node_id == int(a[1]):
                    n2 = node
            e = Edge(n1, n2, distance(n1.pos,n2.pos))
            edges.append(e)
            #all_edges.append(e)
            #edges.append((int(a[0]) - first_value, int(a[1]) - first_value))


    return Graph(nodes, edges, 1)

def graph_to_gdf(graph: Graph, filename: str) -> None:
    """ Write internal graph to gdf file, requires graph nodes have keypoints """
    f = open(filename, "w")

    # Node header definition
    f.write("nodedef> name VARCHAR,label VARCHAR,width DOUBLE,height DOUBLE,x DOUBLE,y DOUBLE,color VARCHAR\n")

    # Write nodes
    i = 1
    px,py = (0.0,0.0)
    #kps = [node.kp for node in graph.nodes]
    for node in graph.nodes:
        (x,y) = node.pos

        # Do not write duplicate keypoints
        if not (x,y) == (px,py):
            f.write(str(i)+"," +
                    "\"" + str(node.label) + "\"," + 
                    str(node.size)+"," +
                    str(node.size)+"," +
                    str(x) + "," + str(y) +
                    ",'153,153,153'\n")
            i += 1

        (px,py) = (x,y)
        f.flush()

    # Edge header definition
    f.write("edgedef> node1,node2,weight DOUBLE,directed BOOLEAN,color VARCHAR\n")

    for edge in graph.edges:
        node1 = edge.n1
        node2 = edge.n2

        f.write(str(node1.node_id) + "," + str(node2.node_id) + ",")

        d = distance(node1.pos, node2.pos)
        f.write(str(d) + "," + "false,'128,128,128'\n")
    
    f.flush()
    f.close()
