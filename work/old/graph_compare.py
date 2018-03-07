import networkx as nx

import matplotlib.pyplot as plt


#https://stackoverflow.com/questions/12122021/python-implementation-of-a-graph-similarity-grading-algorithm
def select_k(spectrum, minimum_energy = 0.9):
    running_total = 0.0
    total = sum(spectrum)
    if total == 0.0:
        return len(spectrum)
    for i in range(len(spectrum)):
        running_total += spectrum[i]
        if running_total / total >= minimum_energy:
            return i + 1
    return len(spectrum)

def eigensim(G1, G2):
    laplacian1 = nx.spectrum.laplacian_spectrum(G1)
    laplacian2 = nx.spectrum.laplacian_spectrum(G2)

    k1 = select_k(laplacian1)
    k2 = select_k(laplacian2)
    k = min(k1, k2)

    return sum((laplacian1[:k] - laplacian2[:k])**2)

print("Start")

G = nx.Graph()
G.add_edge('1','2')
G.add_edge('2', '3')


G2 = nx.Graph()
G2.add_edge('1', '2')
G2.add_edge('1', '3')

print(eigensim(G, G2))

print("End")
