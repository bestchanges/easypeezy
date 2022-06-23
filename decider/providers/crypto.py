"""
Cryptocurrencies providers.
"""

import logging
from typing import Any

from decider.core import Graph, Node, Edge, EdgeRaw

logger = logging.getLogger(__name__)

class BinanceEdge(Edge):

    def __init__(self, ticker, market, **data: Any) -> None:
        super().__init__(**data)
        self.ticker = ticker
        self.market = market
        self.fee

    def url(self):
        return 'http://egor.spb.ru'

def add_quotes_to_graph(tickers, markets, graph: Graph):
    market_by_symbold = {v['symbol']: v for v in markets}
    for ticker in tickers.values():
        symbol = ticker['symbol']
        if not ticker['bid'] or not ticker['ask']:
            logger.warning(f'Skipping zero-price symbol {symbol}')
            continue

        assets = symbol.split('/')
        assert len(assets) == 2, f"Symbol {symbol} should be XXX/YYY"
        base = Node(currency=assets[0])
        quote = Node(currency=assets[1])

        market = market_by_symbold[symbol]
        fee = float(market['taker'])

        edge_direct = EdgeRaw(from_=base, to=quote, price=float(ticker['ask']), fee=fee)
        graph.add(edge_direct)

        edge_reverse = EdgeRaw(from_=quote, to=base, price=1 / float(ticker['bid']), fee=fee)
        graph.add(edge_reverse)
