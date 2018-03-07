import os
import math
from common_graph import *

path = "graphs/annotated/"
is_node = True

i = 0
for graph_file in sorted(os.listdir(path)):
    f = open(path + graph_file)
    print(graph_file)

    lines = f.read().splitlines()[1:]
    graph = translate_graph(lines)
    
    graph_to_gdf(graph, "graphs/complete/" + str(i) + ".gdf")
    i += 1




