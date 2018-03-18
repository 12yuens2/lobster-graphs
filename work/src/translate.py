import sys
import os
import numpy as np

import common.graph as cg

all_edges = []
all_graphs = []

juv_in_path = "graphs/annotated/juvenile/"
mat_in_path = "graphs/annotated/mature/"

juv_out_path = "graphs/complete/juvenile/"
mat_out_path = "graphs/complete/mature/"



def complete_graph(input_path, output_path):
    i = 0
    for annotated_gdf in sorted(os.listdir(input_path)):
        print(annotated_gdf)
        f = open(input_path + annotated_gdf)
        lines = f.read().splitlines()[1:]

        graph = cg.translate_graph(lines)
        cg.graph_to_gdf(graph, output_path + str(i) + ".gdf")

        i += 1



        
complete_graph(juv_in_path, juv_out_path)
complete_graph(mat_in_path, mat_out_path)
