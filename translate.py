import sys
import os
from probability import *

output = open("output.gfu", "w")

all_edges = []
i = 0
j = 0
for f in os.listdir(sys.argv[1]):
    input_file = open(sys.argv[1] + f)

    lines = input_file.read().splitlines()[1:]

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

            n = Node(a[0], a[1], 0)
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


    j += len(nodes)

    output.write("#graph" + str(i) + "\n")
    output.write(str(len(nodes)) + "\n")
    for n in nodes:
        output.write(str(n.label) + "\n")


    output.write(str(len(edges)) + "\n")
    for e in edges:
        output.write(str(e.n1.node_id) + " " + str(e.n2.node_id) + "\n")
    i += 1
    
# create db for edge distributions
edge_db = {}
for edge in all_edges:
    
