import logging
from typing import List, Set, Optional

from pydantic import BaseModel
from pydantic.fields import defaultdict, DefaultDict

logger = logging.getLogger(__name__)


class Node(BaseModel):
    currency: str

    def __hash__(self) -> int:
        return hash(self.currency)


class Edge:
    def __init__(self, from_: Node, to: Node):
        self.from_ = from_
        self.to = to

    def commission(self, amount: float = 1) -> float:
        return 0

    def converted(self, amount: float = 1) -> float:
        return amount

    def url(self) -> Optional[str]:
        pass


class EdgeRaw(Edge):
    def __init__(self, from_: Node, to: Node, price: float, fee: float = 0):
        self.from_ = from_
        self.to = to
        self.price = price
        self.fee = fee

    def converted(self, amount: float = 1) -> float:
        # I have a feeling this calculates incorrectly for case of "1/bid"
        # TODO: check it
        return self.price * amount * (1 - self.fee)

    def __repr__(self) -> str:
        return str([self.from_, self.to, self.price, self.fee])

    def __eq__(self, o: object) -> bool:
        return isinstance(o, EdgeRaw) and self.from_ == o.from_ and self.to == o.to and self.price == o.price and self.fee == o.fee


class Graph():

    def __init__(self):
        self._nodes: Set[Node] = set()
        self._edges: List[Edge] = list()
        self._node_outs: DefaultDict[Node, List[Edge]] = defaultdict(list)

    def paths(self, from_currency: str, to_currency: str, max_length=4) -> List[List[Edge]]:
        from_ = Node(currency=from_currency)
        to = Node(currency=to_currency)
        return self.paths_recursive(from_node=from_, to_node=to, max_length=max_length)

    def add(self, edge: Edge):
        assert edge
        assert edge.from_
        assert edge.to
        self._nodes.add(edge.from_)
        self._nodes.add(edge.to)
        self._edges.append(edge)
        self._node_outs[edge.from_].append(edge)

    def __from_node(self, node: Node) -> List[Edge]:
        return self._node_outs[node]

    def paths_recursive(self, from_node: Node, to_node: Node, max_length: int, edges: List[Edge] = None) -> List[List[Edge]]:
        edges = edges if edges else []
        if from_node == to_node:
            return [edges]
        if len(edges) >= max_length:
            return []
        found_paths = []
        for edge in self.__from_node(from_node):
            new_edges = list(edges)
            new_edges.append(edge)
            found_paths += self.paths_recursive(
                from_node=edge.to,
                to_node=to_node,
                max_length=max_length,
                edges=new_edges
            )
        return found_paths
