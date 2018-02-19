import itertools
import math
import common_cv

class Node():
    def __init__(self, node_id, label, size, kp=None): #probability):
        self.node_id = int(node_id)
        self.label = label
        self.size = size
        self.kp = kp
        #self.probability = probability

    def __repr__(self):
        return str(self.node_id)
        #return str(self.node_id) + ": (" + str(self.label) + ", " + str(self.probability) + ")"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.label == other.label and
                    (within_value(self.size, other.size) or
                     within_value(other.size, self.size)))
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


    def __hash__(self):
        return self.label.__hash__()


class Edge():
    def __init__(self, node1, node2, length):
        self.n1 = node1
        self.n2 = node2
        self.length = length
        #ratio

    def __repr__(self):
        return str(self.n1.node_id) + " " + str(self.n2.node_id)
        #return str(self.n1) + "--" + str(self.n2) + ", " + str(self.length)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            # Both node labels are the same and length is similar values
            return (((self.n1 == other.n1 and self.n2 == other.n2) or
                    (self.n1 == other.n2 and self.n2 == other.n2)) and
                    (within_value(self.length, other.length) or
                     within_value(other.length, self.length)))
                    
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


    def __hash__(self):
        return self.n1.__hash__() + self.n2.__hash__()

        
class Graph():
    def __init__(self, nodes, edges, probability_assignment):
        self.nodes = nodes
        self.edges = edges

        self.prob_a = probability_assignment

    def __repr__(self):
        return str(self.nodes) + " | " + str(self.edges) + " : " + str(self.prob_a)


    def get_node(self, node_id):
        for node in self.nodes:
            if node.node_id == node_id:
                return node

    def write_to(self, file, id):
        """ Write graph for graphgrep query format """
        file.write("#graph" + str(id) + "\n")

        file.write(str(len(self.nodes)) + "\n")
        for node in self.nodes:
            file.write(node.label + "\n")

        file.write(str(len(self.edges)) + "\n")
        for edge in self.edges:
            file.write(str(edge) + "\n")


    def export(self, filename, id):
        f = open(filename, "w")
        self.write_to(f, id)
        f.close()



### Useful functions ###

def within_value(v1, v2):
    """ Check if actual_value is within 20% of target value """
    percentage = 0.2
    error_allowed = percentage * v1
    high = v1 + error_allowed
    low = v1 - error_allowed

    return low <= v2 <= high


def graph_from_permutation(permutation):
    """ Take permutation of n (keypoint, label) tuples and turn into a graph object """
    nodes = []
    for i in range(len(permutation)):
        nodes.append(Node(i, permutation[i][1], permutation[i][0].size, kp=permutation[i][0]))

    edges = []
    for n1,n2 in zip(nodes[:-1], nodes[1:]):
        edges.append(Edge(n1, n2, common_cv.get_distance(n1.kp, n2.kp)))

    return Graph(nodes, edges, 0)

def translate_graph(lines):
    """ Translate graph from gdf to graphgrep query format """
    nodes = []
    edges = []
    is_node = True

    # first_value used to offset node/edge ids to start from 0
    first = True
    first_value = 0

    for line in lines:
        a = line.split(",")

        if "edge" in line:
            is_node = False
        elif is_node:
            if first:
                first = False
                first_value = int(a[0])

            # Create node with Node(id, label, size)
            n = Node(a[0], str(a[1]).replace("\"", ""), float(a[2]))

            if (a[1] == ""):
                print("Node " + a[0] + " missing label.")
                sys.exit()
            nodes.append(n)
        else:
            n1 = None
            n2 = None
            for node in nodes:
                if node.node_id == int(a[0]):
                    n1 = node
            for node in nodes:
                if node.node_id == int(a[1]):
                    n2 = node
            e = Edge(n1, n2, a[3])
            edges.append(e)
            #all_edges.append(e)
            #edges.append((int(a[0]) - first_value, int(a[1]) - first_value))


    return Graph(nodes, edges, 1)




