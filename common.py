from datetime import timedelta
from decimal import Decimal
from typing import List, Optional

import ccxt
from pydantic import BaseModel
from requests_cache import install_cache

import c2c
from core import Graph, Path
from crypto import add_quotes_to_graph


def install_requests_cache():
    default_expire_after = timedelta(hours=1)
    urls_expire_after = {
        'c2c.binance.com/bapi/c2c/v2/friendly/c2c/portal/config': timedelta(days=3),
        'c2c.binance.com/bapi/c2c/v2/friendly/c2c/adv/search': timedelta(minutes=30),
        'api.binance.com/api/v3/exchangeInfo': timedelta(days=3),
        'api.binance.com/api/v3/ticker/24hr': timedelta(minutes=30),
    }

    install_cache(
        cache_name='cache',
        expire_after=default_expire_after,
        urls_expire_after=urls_expire_after,
        allowable_methods=['GET', 'POST'],
    )


def prepare():
    # load binance crypto quotes
    graph = Graph()
    binance = ccxt.binance()
    add_quotes_to_graph(
        tickers=binance.fetch_tickers(),
        markets=binance.fetch_markets(),
        graph=graph
    )
    return graph


def load_c2c_to_graph(fiat_from, fiat_to, graph):
    # load binance C2C quotes
    for offers in c2c.load_binance_c2c_offers(fiat=fiat_from, trade_type='BUY').values():
        c2c.add_c2c_offers_to_graph(offers, graph)
    for offers in c2c.load_binance_c2c_offers(fiat=fiat_to, trade_type='SELL').values():
        c2c.add_c2c_offers_to_graph(offers, graph)


def find_paths_for_fiat(fiat_from, fiat_to, graph, max_length):
    load_c2c_to_graph(fiat_from, fiat_to, graph)

    paths = graph.best_path(
        from_currency=f'{fiat_from}(f)',
        to_currency=f'{fiat_to}(f)',
        max_length=max_length
    )
    return paths


def ordered_paths(path_rates: List[Path]) -> List[Path]:
    """Re-order path rates according to score.
    Consideration
    1. conversion rate taken as initial score (including commissions)
    2. each additional hop reduces score by 2%
    3. TODO: take into account possible difficulties of conversion
    """
    return sorted(path_rates, key=lambda x: x.rate * (1 - 0.02) ** len(x.edges), reverse=True)


class Conversion(BaseModel):
    from_currency: str
    from_amount: Decimal
    to_currency: str
    to_amount: Decimal
    rate: Decimal
    url: Optional[str]


class ConversionPath(BaseModel):
    conversion_rate: Decimal
    source_currency: str
    amount_source_currency: Decimal
    target_currency: str
    amount_target_currency: Decimal
    conversions: List[Conversion]


def prepare_conversion_path(path: Path, source_amount=1) -> ConversionPath:
    conversion_path = ConversionPath(
        source_currency=path.edges[0].from_.currency,
        amount_source_currency=source_amount,
        conversion_rate=path.rate,
        target_currency=path.edges[-1].to.currency,
        amount_target_currency=source_amount * path.rate,
        conversions=list(),
    )
    amount = source_amount
    for edge in path.edges:
        converted_amount = edge.converted(amount)
        conversion = Conversion(
            from_currency=edge.from_.currency,
            from_amount=amount,
            to_currency=edge.to.currency,
            to_amount=converted_amount,
            rate=edge.price,
        )
        amount = converted_amount
        conversion_path.conversions.append(conversion)
    return conversion_path


def prepare_conversion_paths(paths: List[Path], source_amount=1) -> List[ConversionPath]:
    result = []
    for path in ordered_paths(paths):
        result.append(prepare_conversion_path(path, source_amount))
    return result
