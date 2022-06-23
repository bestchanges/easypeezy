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


def test_binance_eth_rub(binance_tickers, binance_markets):
    graph = core.Graph()
    crypto.add_quotes_to_graph(tickers=binance_tickers, markets=binance_markets, graph=graph)
    paths = graph.paths(
        from_currency='ETH',
        to_currency='RUB',
        max_length=2
    )
    assert len(paths) == 15
    path = paths[0]
    # assert str(path) == "[[Node(currency='ETH'), Node(currency='BTC'), 0.054813, 0.001], [Node(currency='BTC'), Node(currency='RUB'), 1168501.0, 0.001]]"
    assert path[0].url() == 'https://www.binance.com/ru/trade/ETH_BTC?type=spot'
    assert path[1].url() == 'https://www.binance.com/ru/trade/BTC_RUB?type=spot'
    assert path[0].converted(1000) == 54.813
    assert path[0].converted() == 0.054813
    assert path[0].commission(1000) == 1
    assert path[0].commission() == 0.001
