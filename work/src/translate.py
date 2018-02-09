import sys
import os
import numpy as np
from probability import *

all_edges = []

def get_graph(lines):
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

            # Create node with Node(id, label, probablility)
            n = Node(a[0], str(a[1]).replace("\"", ""), 0)
      
      if (a[1] == ""):
                print("Node " + a[0] + " missing label.")
                sys.exit()
            nodes.append(n)
        else:
            n1 = 0
            n2 = 0
            for node in nodes:
                if node.node_id == a[0]:
                    n1 = node
            for node in nodes:
                if node.node_id == a[1]:
                    n2 = node
            e = Edge(n1, n2, a[3])
            edges.append(e)
            all_edges.append(e)
            #edges.append((int(a[0]) - first_value, int(a[1]) - first_value))
   

    return Graph(nodes, edges, 1)

output = open("output.gfu", "w")

all_graphs = []

i = 0
for f in os.listdir(sys.argv[1]):
    input_file = open(sys.argv[1] + f)
    lines = input_file.read().splitlines()[1:]

    graph = get_graph(lines)
    graph.write_to(output, i)
    
    i += 1
   
# create db for edge distributions
edge_db = {}
for edge in all_edges:
    if not edge in edge_db:
        edge_db[edge] = Distribution((edge.n1, edge.n2), np.random.normal(5, 2, 10).tolist())

name = "query"
n = 0
for ps in g1.permutations(edge_db):
    filename = "query"+str(n)+".querygfu"
    print(ps)
    ps.export(filename, 0)
    n += 1
