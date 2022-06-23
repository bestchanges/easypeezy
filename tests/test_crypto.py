import ccxt
import pytest
import vcr

from decider import core
from decider.providers import crypto


@pytest.fixture
@vcr.use_cassette('cassettes/fixtures/binance.yaml')
def binance_tickers():
    yield ccxt.binance().fetch_tickers()


@pytest.fixture
@vcr.use_cassette('cassettes/fixtures/binance.yaml')
def binance_markets():
    yield ccxt.binance().fetch_markets()


def ticker(symbol, bid, ask):
    return dict(
        symbol=symbol,
        id=symbol,
        taker=0.001,  # comission
        ask=ask,  # SELL price (> bid)
        bid=bid,  # BUY price
    )


tickers = (
    ticker('ETH/BTC', 0.052, 0.054),
    ticker('EOS/ETH', 0.00086, 0.00088),
    # ETH/USDT ETH=base USDT=quote
    ticker('ETH/USDT', 1095, 1096),
    ticker('BTC/USDT', 20200.0, 20230.0),
)

markets = [
    {'symbol': 'ETH/BTC', 'taker': 0.01},
    {'symbol': 'EOS/ETH', 'taker': 0.01},
    {'symbol': 'ETH/USDT', 'taker': 0.01},
    {'symbol': 'BTC/USDT', 'taker': 0.1},
]


def test_binance_eth_rub(binance_tickers, binance_markets):
    graph = core.Graph()
    crypto.add_quotes_to_graph(tickers=binance_tickers, markets=binance_markets, graph=graph)
    paths = graph.best_path(
        from_currency='ETH',
        to_currency='RUB',
        max_length=2
    )
    assert len(paths) > 0
