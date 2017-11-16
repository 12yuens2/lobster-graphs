class Node():
    def __init__(self, id, labels):
        self.id = id
        self.labels = labels


class Edge():
    def __init__(self, node1, node2, length):
        self.n1 = node1
        self.n2 = node2
        self.length = length


class Graph():
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges


class Distribution():
    def __init__(self, label_tuple, 

n1 = Node(0, {"claw": 0.8, "tail": 0.2})
n2 = Node(1, {"body": 0.7, "claw": 0.3})
n3 = Node(2, {"claw", 0.6, "head": 0.2, "body": 0.2})

e1 = Edge(n1, n2, 5)
e2 = Edge(n2, n3, 5)

e3 = Edge(n1, n3, 8)
e4 = Edge(n1, n2, 3)

g1 = Graph([n1, n2, n3], [e1, e2])
g2 = Graph([n1, n2, n3], [e3, e4])
