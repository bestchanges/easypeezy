import logging
from datetime import timedelta
from typing import List

import ccxt
import click
from requests_cache import install_cache

import c2c
from core import Path, ordered_paths, Graph
from crypto import add_quotes_to_graph

logging.basicConfig(
    level=logging.INFO,
)


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


def display_path_rates(path_rates: List[Path], amount=1) -> None:
    for path in ordered_paths(path_rates):
        path_visual = '-'.join([e.from_.currency for e in path.edges] + [path.edges[-1].to.currency])
        print(f'{amount * path.rate:.3f}', path_visual)


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


@click.command()
@click.option('--currency-from', default='KZT', help='Source fiat currency.')
@click.option('--currency-to', default='RUB', help='Target currency.')
@click.option('--max-length', default=3, help='Maximum length of conversion chain.')
@click.option('--amount', default=1, help='Amount in source currency.')
def best_path_cli(currency_from, currency_to, max_length, amount):
    """Print best conversion paths."""
    install_requests_cache()
    graph = prepare()
    paths = find_paths_for_fiat(currency_from, currency_to, graph, max_length)
    print(f'Found {len(paths)} paths to convert')
    display_path_rates(paths, amount)


if __name__ == '__main__':
    best_path_cli()
