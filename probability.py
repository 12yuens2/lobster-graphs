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
    def __init__(self, label_tuple, data):
        self.label_tuple = label_tuple
        
        self.dictionary = {}
        self.populate_dictionary(data)
        
    def population_dictionary(self, data):
        sum = 0
        for d in data:
            sum += 1

            if d in self.dictionary:
                self.dictionary[d] += 1
            else:
                self.dictionary[d] = 1

        for (k,v) in self.dictionary.items():
            self.dictionary[k] = v / sum

    def get_probability(self, item):
        if item in self.dictionary:
            return self.dictionary[item]
        else:
            return 0.0


n1 = Node(0, {"claw": 0.8, "tail": 0.2})
n2 = Node(1, {"body": 0.7, "claw": 0.3})
n3 = Node(2, {"claw", 0.6, "head": 0.2, "body": 0.2})

e1 = Edge(n1, n2, 5)
e2 = Edge(n2, n3, 5)

e3 = Edge(n1, n3, 8)
e4 = Edge(n1, n2, 3)

g1 = Graph([n1, n2, n3], [e1, e2])
g2 = Graph([n1, n2, n3], [e3, e4])

distributions = []
distributions.append(Distribution(("claw", "body"), [3,4,3,3,5,4,2]))
distributions.append(Distribution(("tail", "body"), [6,7,5,7,7]))
distributions.append(Distribution(("claw", "head"), [5,4,5,3,3,4,3,4,5]))


