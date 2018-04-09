from typing import Tuple
from cv2 import KeyPoint
from common import graph as cg

class Node():
    def __init__(self,
                 node_id: int,
                 label: str,
                 size: int,
                 kp: KeyPoint=None,
                 pos: Tuple[float, float]=None) -> None:

        self.node_id: int = int(node_id)
        self.label: str = label
        self.size: int = size
        self.kp: KeyPoint = kp
        self.pos: Tuple[float, float] = pos

    def __repr__(self):
        return str(self.label) + ": " + str(self.size)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.label == other.label and
                    (cg.within_value(self.size, other.size) or
                     cg.within_value(other.size, self.size)))
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


    def __hash__(self):
        return self.label.__hash__()

 
