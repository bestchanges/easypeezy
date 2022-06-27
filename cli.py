import logging
from typing import List

import click

from common import (
    install_requests_cache,
    prepare,
    find_paths_for_fiat,
    ConversionPath,
    prepare_conversion_paths,
)

logging.basicConfig(
    level=logging.INFO,
)


def display_path_rates(path_rates: List[ConversionPath], limit_top_n=10) -> None:
    for num, path_rate in enumerate(path_rates):
        if num >= limit_top_n:
            break
        path_visual = "-".join(
            [conversion.from_currency for conversion in path_rate.conversions]
            + [path_rate.conversions[-1].to_currency]
        )
        print(f"{path_rate.amount_target_currency:.1f}", path_visual)


def display_conversion_path_detailed(path: ConversionPath):
    print(f"Source amount: {path.amount_source_currency:.2f} {path.source_currency}")
    print(f"Target amount: {path.amount_target_currency:.2f} {path.target_currency}")
    print(f"Number of conversions: {len(path.conversions)}")
    print("Conversions:")
    for num, conversion in enumerate(path.conversions):
        print(
            f"{num}. {conversion.from_amount:.2f} {conversion.from_currency} -> {conversion.to_amount:.2f} {conversion.to_currency} (rate: {conversion.rate:.5f}) - {conversion.url}"
        )


@click.command()
@click.option("--currency-from", default="KZT", help="Source fiat currency.")
@click.option("--currency-to", default="RUB", help="Target currency.")
@click.option("--max-length", default=3, help="Maximum length of conversion chain.")
@click.option("--amount", default=1, help="Amount in source currency.")
def best_path_cli(currency_from, currency_to, max_length, amount):
    """Print best conversion paths."""
    install_requests_cache()
    graph = prepare()
    paths = find_paths_for_fiat(currency_from, currency_to, graph, max_length)
    print(f"Found {len(paths)} paths to convert (Displaying top 10)")
    conversion_paths = prepare_conversion_paths(paths, amount)
    if conversion_paths:
        display_path_rates(conversion_paths)
        print(f"Best paths:")
        for path in conversion_paths[0:3]:
            print("=" * 50)
            display_conversion_path_detailed(path)


if __name__ == "__main__":
    best_path_cli()
