from typing import Tuple
from cv2 import KeyPoint

class Label():
    def __init__(self, name: str, probability: float) -> None:
        self.name: str = name
        self.probability: float = probability


    def __repr__(self):
        return str(self.name) 



KeyLabel = Tuple[KeyPoint, Label]
