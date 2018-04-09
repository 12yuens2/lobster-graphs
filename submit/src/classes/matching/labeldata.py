from typing import TypeVar, Generic
from classes.graphs import Edge

DictKey = TypeVar('DictKey', str, Edge)

class LabelData(Generic[DictKey]):
    def __init__(self,
                 label: DictKey,
                 distribution,
                 size_distribution,
                 probability: float) -> None:

        self.label: DictKey = label
        self.distribution = distribution
        self.size_distribution = size_distribution
        self.probability: float = probability

    def get_probability(self, size):
        return self.distribution.pdf(size) * self.probability / self.size_distribution.pdf(size)

