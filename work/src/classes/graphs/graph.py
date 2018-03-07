
from typing import List, Optional, Any
from .node import Node
from .edge import Edge


class Graph():
    def __init__(self,
                 nodes: List[Node],
                 edges: List[Edge],
                 probability_assignment: float) -> None:

        self.nodes: List[Node] = nodes
        self.edges: List[Edge] = edges

        self.prob_a = probability_assignment

    def __repr__(self):
        return str(self.nodes) + " | " + str(self.edges) + " : " + str(self.prob_a)


    def get_node(self, node_id: int) -> Optional[Node]:
        for node in self.nodes:
            if node.node_id == node_id:
                return node

        return None

    def get_edge(self, id1: int, id2: int) -> Optional[Edge]:
        for edge in self.edges:
            if ((id1 == edge.n1.node_id and id2 == edge.n2.node_id) or
                (id1 == edge.n2.node_id and id2 == edge.n1.node_id)):
               return edge

        return None

    def write_to(self, file: Any, id: int) -> None:
        """ Write graph for graphgrep query format """
        file.write("#graph" + str(id) + "\n")

        file.write(str(len(self.nodes)) + "\n")
        for node in self.nodes:
            file.write(node.label + "\n")

        file.write(str(len(self.edges)) + "\n")
        for edge in self.edges:
            file.write(str(edge) + "\n")


    def export(self, filename: str, id: int) -> None:
        f = open(filename, "w")
        self.write_to(f, id)
        f.close()

