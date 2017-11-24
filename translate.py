import sys
import os
from probability import *

output = open("output.gfu", "w")
nodes = []
edges = []
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

            v = a[1]
            if (v == ""):
                print("Node " + a[0] + " missing label.")
                sys.exit()
            nodes.append(v)
        else:
            edges.append((int(a[0]) - first_value, int(a[1]) - first_value))


    j += len(nodes)

    output.write("#graph" + str(i) + "\n")
    output.write(str(len(nodes)) + "\n")
    for n in nodes:
        output.write(str(n) + "\n")


    output.write(str(len(edges)) + "\n")
    for e in edges:
        output.write(str(e[0]) + " " + str(e[1]) + "\n")
    i += 1
    
