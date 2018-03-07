from typing import Tuple
from cv2 import KeyPoint

class Node():
    def __init__(self,
                 node_id: int,
                 label: str,
                 size: int,
                 kp: KeyPoint=None,
                 pos: Tuple[float, float]=None) -> None: #probability):

        self.node_id: int = int(node_id)
        self.label: str = label
        self.size: int = size
        self.kp: KeyPoint = kp
        self.pos: Tuple[float, float] = pos
        #self.probability = probability

    def __repr__(self):
        #return str(self.node_id)
        return str(self.label) + ": " + str(self.size)
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

 
