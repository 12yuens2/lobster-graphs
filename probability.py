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

            edges = self.get_new_edges(permutation)

            permutation_graphs.append(Graph(list(permutation), edges, probability_assignment))

        return permutation_graphs

    def get_new_edges(self, node_permutations):
        
        new_edges = []
        for edge in self.edges:
            node1 = 0
            node2 = 0
            for node in node_permutations:
                if node.node_id == edge.n1:
                    node1 = node

            for node in node_permutations:
                if node.node_id == edge.n2:
                    node2 = node

            new_edges.append(Edge(node1, node2, edge.length))

        return new_edges
            
            

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

    def __repr__(self):
        return str(self.n1) + "--" + str(self.n2) + ", " + str(self.length)
        
class Graph():
    def __init__(self, nodes, edges, probability_assignment):
        self.nodes = nodes
        self.edges = edges

        self.prob_a = probability_assignment

    def __repr__(self):
        return str(self.nodes) + " | " + str(self.edges) + " : " + str(self.prob_a)

    def export(self, filename):
        f = open(filename, "w")
        f.write("#graph0\n")

        f.write(str(len(self.nodes)) + "\n")
        for node in self.nodes:
            f.write(node.label + "\n")

        f.write(str(len(self.edges)) + "\n")
        for edge in self.edges:
            f.write(str(edge.n1) + " " + str(edge.n2) + "\n")

        f.close()


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


n1 = PossibleNode(0, {"claw": 0.8, "arm": 0.2})
n2 = PossibleNode(1, {"arm": 0.7, "body": 0.3})
n3 = PossibleNode(2, {"body": 0.6, "head": 0.2, "tail": 0.2})

# Possible edges
e1 = Edge(n1.node_id, n2.node_id, 5)
e2 = Edge(n2.node_id, n3.node_id, 5)

e3 = Edge(n1.node_id, n3.node_id, 8)
e4 = Edge(n1.node_id, n2.node_id, 3)

g1 = PossibleGraph([n1, n2, n3], [e1, e2])
g2 = PossibleGraph([n1, n2, n3], [e3, e4])

'''
distributions = []
distributions.append(Distribution(("claw", "body"), [3,4,3,3,5,4,2]))
distributions.append(Distribution(("tail", "body"), [6,7,5,7,7]))
distributions.append(Distribution(("claw", "head"), [5,4,5,3,3,4,3,4,5]))
'''
