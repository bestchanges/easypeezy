import requests
import vcr

import c2c
from core import Node, Edge
import core


@vcr.use_cassette('cassettes/tests/binance_c2c_buy_kzt.yaml')
def test_load_binance_c2c_offers_buy_kzt():
    fiat = 'KZT'
    trade_type = 'BUY'
    offers = c2c.load_binance_c2c_offers(requests.session(), fiat, trade_type)
    assert set(offers) == {'USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'SHIB'}
    for asset, offers in offers.items():
        assert 0 < len(offers) <= 10


@vcr.use_cassette('cassettes/tests/binance_c2c_sell_rub.yaml')
def test_load_binance_c2c_offers_sell_rub():
    fiat = 'RUB'
    trade_type = 'SELL'
    offers = c2c.load_binance_c2c_offers(requests.session(), fiat, trade_type)
    assert set(offers) == {'USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'SHIB', 'RUB'}
    for asset, offers in offers.items():
        assert len(offers) <= 10


@vcr.use_cassette('cassettes/tests/binance_c2c_sell_rub.yaml')
def test_add_to_graph_sell_rub():
    graph = core.Graph(nodes=set(), edges=[])
    offers = c2c.load_binance_c2c_offers(requests.session(), fiat='RUB', trade_type='SELL')

    c2c.add_c2c_offers_to_graph(offers['USDT'], graph)

    fiat_node = core.Node(currency='RUB(f)')
    asset_node = core.Node(currency='USDT')
    assert graph.nodes == {fiat_node, asset_node}
    assert [core.Edge(from_=asset_node, to=fiat_node, price=61.35, commission=0)] == graph.edges


@vcr.use_cassette('cassettes/tests/binance_c2c_buy_kzt.yaml')
def test_add_to_graph_buy_kzt():
    graph = core.Graph(nodes=set(), edges=[])
    offers = c2c.load_binance_c2c_offers(requests.session(), fiat='KZT', trade_type='BUY')

    c2c.add_c2c_offers_to_graph(offers['USDT'], graph)

    fiat_node = core.Node(currency='KZT(f)')
    asset_node = core.Node(currency='USDT')
    assert graph.nodes == {fiat_node, asset_node}
    assert [core.Edge(from_=fiat_node, to=asset_node, price=0.002187011339653796, commission=0)] == graph.edges


@vcr.use_cassette('cassettes/tests/c2c_test_add_to_graph_all.yaml')
def test_add_to_graph_all():
    graph = core.Graph(nodes=set(), edges=[])
    offers_1 = c2c.load_binance_c2c_offers(requests.session(), fiat='KZT', trade_type='BUY')
    offers_2 = c2c.load_binance_c2c_offers(requests.session(), fiat='RUB', trade_type='SELL')

    for asset_offers in list(offers_1.values()) + list(offers_2.values()):
        c2c.add_c2c_offers_to_graph(asset_offers, graph)

    assert graph.nodes == {
        Node(currency='BUSD'),
        Node(currency='BNB'),
        Node(currency='ETH'),
        Node(currency='BTC'),
        Node(currency='RUB'),
        Node(currency='SHIB'),
        Node(currency='KZT(f)'),
        Node(currency='USDT'),
        Node(currency='RUB(f)')}
    assert len(graph.edges) == 13
