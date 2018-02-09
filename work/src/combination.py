import itertools


class Node():
    def __init__(self, id, label):
        self.id = id
        self.label = label


    def __repr__(self):
        return str(str(self.id) + ": " + self.label)



def possible_node_labels(size):
    

def graph_permutations(nodes):
    
    
test = [i for i in range(30)]

labels = ["a", "b", "c", "d", "e", "f"]

# 1. All node permutations

# 2. All node label combinations

label_combinations = (list(itertools.product(test, labels)))

nodes = []
for lc in label_combinations:
    nodes.append(Node(lc[0], lc[1]))

print(str(nodes[1].id) + ": " + nodes[1].label)

permutations = list(itertools.permutations(nodes, 3))
filtered = list(filter(lambda x: x[0].id != x[1].id, permutations))

print(len(permutations))
print(len(filtered))


