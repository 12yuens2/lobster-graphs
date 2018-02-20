import os
import math
from common_graph import *

path = "graphs/annotated/"
is_node = True
for graph_file in os.listdir(path):
    f = open(path + graph_file)

    lines = f.read().splitlines()[1:]
    graph = translate_graph(lines)
    
    graph_to_gdf(graph, "graphs/complete/" + graph_file)




