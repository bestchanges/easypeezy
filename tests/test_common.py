import common
from decider.core import EdgeRaw, Node

n1 = Node(currency='N1')
n2 = Node(currency='N2')
n3 = Node(currency='N3')

def test_ordered_paths():
    path1 = common.Path(edges=[EdgeRaw(n1, n2, 4, 0.01)])
    path2 = common.Path(edges=[EdgeRaw(n1, n3, 2, 0.01), EdgeRaw(n3, n2, 2.5, 0.01)])
    paths = [
        path1,
        path2,
    ]
    assert (path1.score(), path2.score()) == (3.8808, 4.706440199999999)
    ordered_paths = common.ordered_paths(paths)

    assert ordered_paths == [path2, path1]
