import logging
from functools import lru_cache
from typing import List, Set, Tuple

from pydantic import BaseModel

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


class Graph(BaseModel):
    nodes: Set[Node]
    edges: List[Edge]

    def best_path(self, from_currency: str, to_currency: str, max_length=4) -> List[Path]:
        from_ = Node(currency=from_currency)
        to = Node(currency=to_currency)
        return self.paths_recursive(from_node=from_, to_node=to, max_length=max_length)

    def __from_node(self, node: Node) -> List[Edge]:
        found = []
        for edge in self.edges:
            if edge.from_ == node:
                found.append(edge)
        return found

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


def ordered_paths(path_rates: List[Path]) -> List[Path]:
    """Re-order path rates.

    1. By path length (short goes first)
    2. By price

    """
    return sorted(path_rates, key=lambda x: (-1 * len(x.edges), -1 * x.rate), reverse=True)
