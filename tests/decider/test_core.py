import math
from typing import List

import pytest

from decider.core import Node, Edge, Graph, EdgeRaw
# TODO: get rig of crypto here. Build graph from scratch


def ticker(symbol, bid, ask):
    return dict(
        symbol=symbol,
        id=symbol,
        taker=0.001,  # comission
        ask=ask,  # SELL price (> bid)
        bid=bid,  # BUY price
    )


USDT = Node(currency='USDT')
BTC = Node(currency='BTC')
EOS = Node(currency='EOS')
ETH = Node(currency='ETH')

BTC_ETH = EdgeRaw(from_=BTC, to=ETH, price=19.23, fee=0.01)
ETH_BTC = EdgeRaw(from_=ETH, to=BTC, price=0.0526, fee=0.01)
EOS_ETH = EdgeRaw(from_=EOS, to=ETH, price=0.054, fee=0.01)
ETH_EOS = EdgeRaw(from_=ETH, to=EOS, price=18.518, fee=0.01)
BTC_USDT = EdgeRaw(from_=BTC, to=USDT, price=20230.0, fee=0.1)
USDT_BTC = EdgeRaw(from_=USDT, to=BTC, price=0.00004943, fee=0.1)
ETH_USDT = EdgeRaw(from_=ETH, to=USDT, price=1096.0, fee=0.01)
USDT_ETH = EdgeRaw(from_=USDT, to=ETH, price=0.00091240, fee=0.01)

EDGES = [BTC_ETH, ETH_BTC, EOS_ETH, ETH_EOS, BTC_USDT, USDT_BTC, ETH_USDT, USDT_ETH]

@pytest.mark.parametrize(
    'kwargs, expected, expected_rates',
    [
        # 1-hop ETH to USDT
        [
            dict(from_currency='ETH', to_currency='USDT', max_length=1),
            [
                [ETH_USDT],
            ],
            [1085.039999999999999771849168],
        ],
        # 2-hop ETH to USDT
        [
            dict(from_currency='ETH', to_currency='USDT', max_length=2),
            [
                [ETH_BTC, BTC_USDT],
                [ETH_USDT],
            ],
            [948.1113180000001, 1085.04],
        ],
        # direct 1-hop ETH to BTC
        [
            dict(from_currency='ETH', to_currency='BTC', max_length=1),
            [
                [ETH_BTC],
            ],
            [0.052074],
        ],
        # reverse 1-hop BTC to ETH
        [
            dict(from_currency='BTC', to_currency='ETH', max_length=1),
            [
                [BTC_ETH],
            ],
            [19.0377],
        ],
    ]
)
def test_graph(kwargs, expected: List[Edge], expected_rates):
    graph = Graph()
    for edge in EDGES:
        graph.add(edge)
    paths = graph.paths(**kwargs)
    assert paths == expected
    assert [math.prod([edge.converted() for edge in path]) for path in paths] == expected_rates


# TODO: write test to remove loops in found Path