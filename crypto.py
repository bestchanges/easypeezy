import logging

from core import Graph, Node, Edge

logger = logging.getLogger(__name__)


def build_graph(tickers, markets) -> Graph:
    nodes = set()
    edges = []
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
        nodes.add(base)
        nodes.add(quote)
        market = market_by_symbold[symbol]
        fee = market['taker']

        edge_direct = Edge(from_=base, to=quote, price=ticker['ask'], fee=fee)
        edges.append(edge_direct)

        edge_reverse = Edge(from_=quote, to=base, price=1 / ticker['bid'], fee=fee)
        edges.append(edge_reverse)

    return Graph(edges=edges, nodes=nodes)
