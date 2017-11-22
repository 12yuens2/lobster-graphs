import itertools

class PossibleGraph():
    def __init__(self, possible_nodes, edges):
        self.possible_nodes = possible_nodes
        self.edges = edges

    def permutations(self):

        # Use itertools on possible_nodes to get all combinations of node labels
        permutations = list(itertools.product(*[possible_node.combinations() for possible_node in self.possible_nodes]))
        permutation_graphs = []

        for permutation in permutations:
            probability_assignment = 1
            for node in permutation:
                probability_assignment *= node.probability

            permutation_graphs.append(Graph(list(permutation), self.edges, probability_assignment))

        return permutation_graphs

class PossibleNode():
    def __init__(self, node_id, labels):
        self.node_id = node_id
        self.labels = labels

    def combinations(self):
        return [Node(self.node_id, label, probability) for (label, probability) in self.labels.items()]


class Node():
    def __init__(self, node_id, label, probability):
        self.node_id = node_id
        self.label = label
        self.probability = probability

    def __repr__(self):
        return str(self.node_id) + ": (" + str(self.label) + ", " + str(self.probability) + ")"


class Edge():
    def __init__(self, node1, node2, length):
        self.n1 = node1
        self.n2 = node2
        self.length = length
        
class Graph():
    def __init__(self, nodes, edges, probability_assignment):
        self.nodes = nodes
        self.edges = edges

        self.prob_a = probability_assignment

    def __repr__(self):
        return str(self.nodes) + " | " + str(self.edges) + " : " + str(self.prob_a)



class Distribution():
    def __init__(self, label_tuple, data):
        self.label_tuple = label_tuple
        
        self.dictionary = {}
        self.populate_dictionary(data)
        
    def populate_dictionary(self, data):
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


pn1 = PossibleNode(0, {"a": 0.2, "b": 0.4})
pn2 = PossibleNode(1, {"s": 0.4, "a": 0.8})
pn3 = PossibleNode(2, {"b": 0.5, "c": 0.5, "g": 0.6})
e1 = Edge(0, 1, 5)
e2 = Edge(1, 2, 5)
pg1 = PossibleGraph([pn1, pn2, pn3], [e1, e2])

'''
n1 = PossibleNode(0, {"claw": 0.8, "tail": 0.2})
n2 = PossibleNode(1, {"body": 0.7, "claw": 0.3})
n3 = PossibleNode(2, {"claw": 0.6, "head": 0.2, "body": 0.2})

e1 = Edge(n1, n2, 5)
e2 = Edge(n2, n3, 5)

e3 = Edge(n1, n3, 8)
e4 = Edge(n1, n2, 3)

g1 = PossibleGraph([n1, n2, n3], [e1, e2])
g2 = PossibleGraph([n1, n2, n3], [e3, e4])

distributions = []
distributions.append(Distribution(("claw", "body"), [3,4,3,3,5,4,2]))
distributions.append(Distribution(("tail", "body"), [6,7,5,7,7]))
distributions.append(Distribution(("claw", "head"), [5,4,5,3,3,4,3,4,5]))


'''
