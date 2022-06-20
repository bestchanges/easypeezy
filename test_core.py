import pytest

import crypto
from core import Node, Edge, Path


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

BTC_ETH = Edge(from_=BTC, to=ETH, price=19.23076923076923, fee=0.01)
ETH_BTC = Edge(from_=ETH, to=BTC, price=0.054, fee=0.01)
EOS_ETH = Edge(from_=EOS, to=ETH, price=0.054, fee=0.01)
BTC_USDT = Edge(from_=BTC, to=USDT, price=20230.0, fee=0.1)
ETH_USDT = Edge(from_=ETH, to=USDT, price=1096.0, fee=0.01)

tickers = (
    ticker('ETH/BTC', 0.052, 0.054),
    ticker('EOS/ETH', 0.00086, 0.00088),
    # ETH/USDT ETH=base USDT=quote
    ticker('ETH/USDT', 1095, 1096),
    ticker('BTC/USDT', 20200.0, 20230.0),
)
tickers = {v['symbol']: v for v in tickers}

markets = [
    {'symbol': 'ETH/BTC', 'taker': 0.01},
    {'symbol': 'EOS/ETH', 'taker': 0.01},
    {'symbol': 'ETH/USDT', 'taker': 0.01},
    {'symbol': 'BTC/USDT', 'taker': 0.1},
]


@pytest.mark.parametrize(
    'kwargs, expected, expected_rates',
    [
        # 1-hop ETH to USDT
        [
            dict(from_currency='ETH', to_currency='USDT', max_length=1),
            [
                Path(edges=[Edge(from_=ETH, to=USDT, price=1096.0,
                                 fee=0.01)]),
            ],
            [1085.04],
        ],
        # 2-hop ETH to USDT
        [
            dict(from_currency='ETH', to_currency='USDT', max_length=2),
            [
                Path(edges=[ETH_BTC, BTC_USDT]),
                Path(edges=[ETH_USDT]),
            ],
            [973.34622, 1085.04],
        ],
        # direct 1-hop ETH to BTC
        [
            dict(from_currency='ETH', to_currency='BTC', max_length=1),
            [
                Path(edges=[ETH_BTC]),
            ],
            [0.05346],
        ],
        # reverse 1-hop BTC to ETH
        [
            dict(from_currency='BTC', to_currency='ETH', max_length=1),
            [
                Path(edges=[BTC_ETH]),
            ],
            [19.038461538461537],
        ],
    ]
)
def test_graph(kwargs, expected, expected_rates):
    graph = crypto.build_graph(tickers=tickers, markets=markets)
    path_rates = graph.best_path(**kwargs)
    # core.display_path_rates(path_rates)
    assert path_rates == expected
    assert [v.rate for v in path_rates] == expected_rates
