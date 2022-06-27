"""
Customer to Customer exchange providers.
"""
import logging
import statistics
from typing import List, Dict, Optional

import requests

from decider import core
from decider.core import Edge, Node

logger = logging.getLogger(__name__)


class BinnanceP2PEdge(Edge):
    def __init__(
        self, offers: list, median_price_of_first_n=4
    ):
        """
        :param offers: list of offers. Should be same trade_type, fiat and asset currency
        :param median_price_of_first_n: median value of first N items will be taken as price
        """

        fiat_currency = offers[0]["adv"]["fiatUnit"]
        asset_currency = offers[0]["adv"]["asset"]
        trade_type = offers[0]["adv"]["tradeType"]
        assert trade_type in ("BUY", "SELL")
        assert all([offer["adv"]["tradeType"] == trade_type for offer in offers])
        assert all([offer["adv"]["fiatUnit"] == fiat_currency for offer in offers])
        assert all([offer["adv"]["asset"] == asset_currency for offer in offers])

        fiat_node = core.Node(currency=f"{fiat_currency}(f)")
        asset_node = core.Node(currency=asset_currency)

        prices = [float(item["adv"]["price"]) for item in offers]
        median_price = statistics.median(prices[:median_price_of_first_n])
        assert median_price > 0

        if trade_type == "BUY":
            # base:USDT / quote:KZT 450    - trade_type == BUY
            # buy crypto (base) for fiat (quote)
            base = asset_node
            quote = fiat_node
            price = median_price
        else:
            # base:USDT / quote:KZT 450    - trade_type == SELL
            base = fiat_node
            quote = asset_node
            price = 1 / median_price

        self.trade_type = trade_type
        self.fiat = fiat_currency
        self.asset = asset_currency

        self.price = price
        self.offers = offers

        super().__init__(base, quote)

    def commission(self, amount: float = 1) -> float:
        return 0

    def converted(self, amount: float = 1) -> float:
        return amount * self.price

    def url(self) -> Optional[str]:
        if self.trade_type == 'SELL':
            url = f'https://c2c.binance.com/ru/trade/all-payments/{self.asset}?fiat={self.fiat}'
        else:
            url = f'https://c2c.binance.com/ru/trade/sell/{self.asset}?fiat={self.fiat}&payment=ALL'
        return url

    def __repr__(self) -> str:
        return str([self.from_, self.to, self.converted(), self.commission()])


def binance_c2c_search(
    fiat: str,
    asset: str,
    trade_type: str,
    pay_types=(),
    countries=(),
    publisher_type=None,
    rows=10,
    page=1,
):
    """
    Search for C2C offers.

    :param fiat: fiat currency like 'KZT'
    :param asset: crypto currency like 'USDT'
    :param trade_type: 'BUY' or 'SELL' crypto for fiat
    :param pay_types: list of strings payment types, like ["KaspiBank"]
    :param countries: list of strings countries like ["KZ"]
    :param publisher_type: None for any, 'merchant' for only from merchants.
    :param rows: number or items to return
    :param page: page number. Starts with 1.
    :return:
    """
    assert fiat
    assert asset
    assert trade_type in ("BUY", "SELL")
    request_payload = {
        "page": page,
        "rows": rows,
        "payTypes": pay_types,
        "countries": countries,
        "publisherType": publisher_type,
        "asset": asset,
        "fiat": fiat,
        "tradeType": trade_type,
    }
    r = requests.post(
        "https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/adv/search",
        json=request_payload,
    )
    r.raise_for_status()
    response_payload = r.json()
    return response_payload


def binance_c2c_config(fiat: str):
    assert fiat
    request_payload = {
        "fiat": fiat,
    }
    r = requests.post(
        "https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/portal/config",
        json=request_payload,
    )
    r.raise_for_status()
    response_payload = r.json()

    return response_payload


def load_binance_c2c_offers(fiat: str, trade_type: str, max_offers=10):
    logger.info(f"Loading config for {fiat}")
    c2c_config = binance_c2c_config(
        fiat=fiat,
    )
    areas = {v["area"]: v for v in c2c_config["data"]["areas"]}
    trade_sides = {v["side"]: v for v in areas["P2P"]["tradeSides"]}

    asset_offers = {}
    for asset in trade_sides[trade_type]["assets"]:
        asset_name = asset["asset"]
        logger.info(f"Loading offers for {asset_name}")
        offers = binance_c2c_search(
            fiat=fiat, asset=asset_name, trade_type=trade_type, rows=max_offers
        )["data"]
        logger.info(
            f"Loaded {len(offers)} offers for P2P {trade_type} {fiat} to {asset_name}"
        )
        asset_offers[asset_name] = offers
    return asset_offers


def add_c2c_offers_to_graph(
    offers: List[Dict], graph: core.Graph,
):
    """
    Register C2C offers in graph.

    :param offers: list of offers. Should be same trade_type, fiat and asset currency
    :param graph:
    :param median_price_of_first_n: median value of first N items will be taken as price
    :return:
    """
    if not offers:
        return

    edge = BinnanceP2PEdge(offers=offers)
    graph.add(edge)
