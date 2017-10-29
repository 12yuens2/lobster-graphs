import sys
import os

print("args: " + str(sys.argv))


output = open("output.lne", "w")

i = 0
for f in os.listdir(sys.argv[1]):
    input_file = open(sys.argv[1] + f)

    lines = input_file.read().splitlines()[1:]

    nodes = []
    edges = []

    is_node = True
    for line in lines:
        a = line.split(",")
        if "edge" in line:
            is_node = False
        elif is_node:
            nodes.append(int(a[0]))
        else:
            edges.append((int(a[0]), int(a[1])))

    output.write("#graph" + str(i) + "\n")
    output.write(str(len(nodes)) + "\n")
    for n in nodes:
        output.write(str(n) + "\n")


    output.write(str(len(edges)) + "\n")
    for e in edges:
        output.write(str(e[0]) + " " + str(e[1]) + "\n")
    output.write("\n")
    i += 1
    
print(nodes)
print(edges)
