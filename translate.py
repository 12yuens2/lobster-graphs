input = open("graphs/lobster1388.gdf")
output = open("output.lne", "w")

lines = input.read().splitlines()[1:]

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

output.write("#graph0\n")
output.write(str(len(nodes)) + "\n")
for n in nodes:
    output.write(str(n) + "\n")


output.write(str(len(edges)) + "\n")
for e in edges:
    output.write(str(e[0]) + " " + str(e[1]) + "\n")
   
print(nodes)
print(edges)


