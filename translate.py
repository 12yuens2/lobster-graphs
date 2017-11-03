import sys
import os

print("args: " + str(sys.argv))


output = open("output.gfu", "w")

i = 0
j = 0
for f in os.listdir(sys.argv[1]):
    for x in range(100):
        input_file = open(sys.argv[1] + f)

        lines = input_file.read().splitlines()[1:]

        nodes = []
        edges = []

        is_node = True
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

                nodes.append(int(a[0]) - first_value + j)
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
    
print(nodes)
print(edges)
