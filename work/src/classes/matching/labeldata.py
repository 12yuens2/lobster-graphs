from typing import TypeVar, Generic
from classes.graphs import Edge

DictKey = TypeVar('DictKey', str, Edge)

class LabelData(Generic[DictKey]):
    def __init__(self, label: DictKey, distribution, probability: float) -> None:
        self.label: DictKey = label
        self.distribution = distribution
        self.probability: float = probability

    def get_probability(self, value):
        p = self.distribution.pdf(value) * self.probability
        return p

