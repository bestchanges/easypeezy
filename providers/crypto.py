"""
Cryptocurrencies providers.
"""

import logging

from decider.core import Graph, Node, Edge

logger = logging.getLogger(__name__)


class BinanceEdge(Edge):
    def __init__(
        self, from_: Node, to: Node, ticker: dict, market: dict, is_direct: bool
    ):
        super().__init__(from_, to)
        self.ticker = ticker
        self.market = market
        self.is_direct = is_direct

    def commission(self, amount: float = 1) -> float:
        return amount * self.market["taker"]

    def converted(self, amount: float = 1) -> float:
        price = self.ticker["ask"] if self.is_direct else 1 / self.ticker["bid"]
        return amount * price

    def url(self):
        return f'https://www.binance.com/ru/trade/{self.market["base"]}_{self.market["quote"]}?type=spot'

    def __repr__(self) -> str:
        return str([self.from_, self.to, self.converted(), self.commission()])


def add_quotes_to_graph(tickers, markets, graph: Graph):
    market_by_symbold = {v["symbol"]: v for v in markets}
    for ticker in tickers.values():
        symbol = ticker["symbol"]
        if not ticker["bid"] or not ticker["ask"]:
            logger.debug(f"Skipping zero-price symbol {symbol}")
            continue

        assets = symbol.split("/")
        assert len(assets) == 2, f"Symbol {symbol} should be XXX/YYY"
        base = Node(currency=assets[0])
        quote = Node(currency=assets[1])

        market = market_by_symbold[symbol]

        edge_direct = BinanceEdge(
            from_=base, to=quote, ticker=ticker, market=market, is_direct=True
        )
        graph.add(edge_direct)

        edge_reverse = BinanceEdge(
            from_=quote, to=base, ticker=ticker, market=market, is_direct=False
        )
        graph.add(edge_reverse)
