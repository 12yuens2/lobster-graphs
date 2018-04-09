import os
import sys
import cv2
import numpy as np

import common.graph as cg
import common.cv as cc
import common.write as cw

category = sys.argv[1]
image_path = "imgs/dataset/" + category + "/raw/"
write_path = "imgs/dataset/" + category + "/annotated/"
graph_path = "graphs/annotated/" + category + "/"

# Get annotated .gdf files as graph objects
for gdf_filename in os.listdir(graph_path):

    # Image name is IMG_[0-9]+.JPG and gdf file name is [0-9]+.gdf
    image_name = "IMG_" + gdf_filename.split(".")[0] + ".JPG"

    # Get graph from .gdf file
    gdf_file = open(graph_path + gdf_filename, "r")
    graph = cg.translate_graph(gdf_file.read().splitlines()[1:])

    cw.write_graph(graph, image_name, image_path, write_path)

    print("Wrote " + image_name)
