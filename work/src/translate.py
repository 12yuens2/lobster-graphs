import sys
import os
import numpy as np

import common.graph as cg

#all_edges = []
#all_graphs = []

juv_in_path = "graphs/annotated/juvenile/"
mat_in_path = "graphs/annotated/mature/"

juv_out_path = "graphs/complete/juvenile/"
mat_out_path = "graphs/complete/mature/"


# Translates between an incomplete .gdf with nodes and edges to complete .gdf edges
def complete_graph(input_path, output_path, gfu_filename):
    gfu_file = open(gfu_filename, "w")
    
    i = 0
    for annotated_gdf in sorted(os.listdir(input_path)):
        print(annotated_gdf)
        f = open(input_path + annotated_gdf)
        lines = f.read().splitlines()[1:]

        # Get Graph object from file lines
        graph = cg.translate_graph(lines)

        # Write graph back to .gdf
        cg.graph_to_gdf(graph, output_path + str(i) + ".gdf")

        # Append graph to .gfu for graphgrep database with labels instead of node ids
        graph.write_to(gfu_file, i)

        gfu_file.flush()
        i += 1

    gfu_file.close()

        
complete_graph(juv_in_path, juv_out_path, "juvenile.gfu")
complete_graph(mat_in_path, mat_out_path, "mature.gfu")
