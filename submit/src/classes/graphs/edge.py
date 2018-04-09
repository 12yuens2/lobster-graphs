#import common.graph as cg
from common import graph as cg

from .node import Node

class Edge():
    def __init__(self, node1: Node, node2: Node, length: int) -> None:
        self.n1: Node = node1
        self.n2: Node = node2
        self.length: int = length

    def __repr__(self):
        return str(int(self.n1.node_id) - 1) + " " + str(int(self.n2.node_id) - 1)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            # Both node labels are the same and length is similar values
            return (((self.n1.label == other.n1.label and self.n2.label == other.n2.label) or
                    (self.n1.label == other.n2.label and self.n2.label == other.n1.label)) and
                    (cg.within_value(self.length, other.length) or
                     cg.within_value(other.length, self.length)))
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


    def __hash__(self):
        return self.n1.__hash__() + self.n2.__hash__()

 
