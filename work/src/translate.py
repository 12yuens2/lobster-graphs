import sys
import os
import numpy as np
from common_graph import *

all_edges = []

output = open("output.gfu", "w")

all_graphs = []

i = 0
for f in os.listdir(sys.argv[1]):
    input_file = open(sys.argv[1] + f)
    lines = input_file.read().splitlines()[1:]

    graph = get_graph(lines)
    graph.write_to(output, i)
    
    i += 1
   
# create db for edge distributions
edge_db = {}
for edge in all_edges:
    if not edge in edge_db:
        edge_db[edge] = Distribution((edge.n1, edge.n2), np.random.normal(5, 2, 10).tolist())

name = "query"
n = 0
for ps in g1.permutations(edge_db):
    filename = "query"+str(n)+".querygfu"
    print(ps)
    ps.export(filename, 0)
    n += 1
