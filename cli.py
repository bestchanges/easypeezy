import logging
from typing import List

import click

from common import install_requests_cache, prepare, find_paths_for_fiat
from core import Path, ordered_paths

logging.basicConfig(
    level=logging.INFO,
)


def display_path_rates(path_rates: List[Path], amount=1) -> None:
    for path in ordered_paths(path_rates):
        path_visual = '-'.join([e.from_.currency for e in path.edges] + [path.edges[-1].to.currency])
        print(f'{amount * path.rate:.3f}', path_visual)


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
