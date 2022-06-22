import logging
from functools import lru_cache
from typing import List, Set, Tuple

from pydantic import BaseModel
from pydantic.fields import defaultdict, DefaultDict

logger = logging.getLogger(__name__)


class Node(BaseModel):
    currency: str

    def __hash__(self) -> int:
        return hash(self.currency)


class Edge(BaseModel):
    from_: Node
    to: Node
    price: float
    fee: float = 0

    def converted(self, amount: float = 1):
        # I have a feeling this calculates incorrectly for case of "1/bid"
        # TODO: check it
        return self.price * amount * (1 - self.fee)

    def __hash__(self) -> int:
        return hash((self.from_, self.to, self.price, self.fee))


# TODO: remove Path. List[Edge] will be enough
class Path(BaseModel):
    edges: Tuple[Edge, ...]

    @property
    @lru_cache()
    def rate(self):
        price = 1
        for edge in self.edges:
            price *= edge.converted(1)
        return price

    def __hash__(self) -> int:
        return hash(self.edges)


class Graph():

    def __init__(self):
        self._nodes: Set[Node] = set()
        self._edges: List[Edge] = list()
        self._node_outs: DefaultDict[Node, List[Edge]] = defaultdict(list)

    def best_path(self, from_currency: str, to_currency: str, max_length=4) -> List[Path]:
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

    def paths_recursive(self, from_node: Node, to_node: Node, max_length: int, edges: List[Edge] = None) -> List[Path]:
        edges = edges if edges else []
        if from_node == to_node:
            return [Path(edges=tuple(edges))]
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


