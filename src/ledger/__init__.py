"""ledger: balances and spending from a CSV file of transactions."""

import argparse
import csv
from collections import defaultdict
from decimal import Decimal

from rich.console import Console
from rich.table import Table


def read_transactions(path):
    """Reads the CSV file and returns one dict per row, with the amount as a Decimal."""
    with open(path, newline="") as f:
        transactions = list(csv.DictReader(f))
    for t in transactions:
        t["amount"] = Decimal(t["amount"])
    return transactions


def totals_by(transactions, column):
    """Adds up the amounts for each value of `column` (account, category...)."""
    totals = defaultdict(Decimal)
    for t in transactions:
        totals[t[column]] += t["amount"]
    return dict(totals)


def main() -> None:
    parser = argparse.ArgumentParser(prog="ledger", description=__doc__)
    parser.add_argument("command", choices=["balance", "spending", "months"])
    parser.add_argument("file", nargs="?", default="data/transactions.csv")
    args = parser.parse_args()

    transactions = read_transactions(args.file)
    if args.command == "balance":
        for account, total in sorted(totals_by(transactions, "account").items()):
            print(f"{account:<10} {total:>10}")
    elif args.command == "months":
        # Optional Lab 4 challenge: net change per month (YYYY-MM)
        for t in transactions:
            t["month"] = t["date"][:7]
        for month, total in sorted(totals_by(transactions, "month").items()):
            print(f"{month:<10} {total:>10}")
    else:
        spending = [
            t for t in transactions if t["amount"] < 0 and t["category"] != "transfer"
        ]
        table = Table(title="Spending by category")
        table.add_column("Category")
        table.add_column("EUR", justify="right")
        for category, total in sorted(
            totals_by(spending, "category").items(), key=lambda item: item[1]
        ):
            table.add_row(category, f"{-total:,.2f}")
        Console().print(table)
