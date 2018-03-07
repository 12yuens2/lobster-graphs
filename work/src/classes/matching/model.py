
class Model():
    def __init__(self, labels):
        self.labels = labels.copy()
        self.triplets = []

    def __repr__(self):
        return str(self.labels) + "\n" + str(self.triplet)
        
    def check_nodes(self, nodes):
        for kp,label in nodes:
            if kp in [t[0] for t in self.triplets]:
                return False
            #elif label.name in self.labels and self.labels[label.name] <= 0:
                # bug if count is 1 but two instances of that label in nodes
                #return False
        return True

    def add_nodes(self, nodes):
        self.triplets += nodes

        for kp,label in nodes:
            self.labels[label.name] -= 1

    def add_if_valid(self, nodes):
        if self.check_nodes(nodes):
            self.add_nodes(nodes)

