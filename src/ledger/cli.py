"""The command line: reads the arguments, calls storage and reports, prints."""

import argparse
from decimal import Decimal
from pathlib import Path

from rich.console import Console
from rich.table import Table

from ledger import reports, storage

DEFAULT_FILE = Path("data/transactions.csv")


def print_totals(totals: dict[str, Decimal]) -> None:
    for name, total in totals.items():
        print(f"{name:<10} {total:>10}")


def print_spending(spending: dict[str, Decimal]) -> None:
    table = Table(title="Spending by category")
    table.add_column("Category")
    table.add_column("EUR", justify="right")
    for category, total in spending.items():
        table.add_row(category, f"{total:,.2f}")
    Console().print(table)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ledger", description="Balances and spending of your accounts."
    )
    parser.add_argument("command", choices=["balance", "spending", "months"])
    parser.add_argument("file", nargs="?", type=Path, default=DEFAULT_FILE)
    args = parser.parse_args()

    transactions = storage.read_csv(args.file)
    if args.command == "balance":
        print_totals(reports.balances(transactions))
    elif args.command == "spending":
        print_spending(reports.spending_by_category(transactions))
    elif args.command == "months":
        print_totals(reports.net_by_month(transactions))
