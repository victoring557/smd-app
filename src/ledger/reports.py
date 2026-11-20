"""Calculations on transactions. No files, no printing: data in, data out."""

from collections import defaultdict
from collections.abc import Callable, Iterable
from decimal import Decimal

from ledger.models import Transaction

TRANSFER = "transfer"


def totals_by(
    transactions: Iterable[Transaction], key: Callable[[Transaction], str]
) -> dict[str, Decimal]:
    """Adds up the amounts of the transactions for each value of `key`."""
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for t in transactions:
        totals[key(t)] += t.amount
    return dict(totals)


def is_spending(t: Transaction) -> bool:
    """Money that left the accounts: negative, and not a transfer between them."""
    return t.amount < 0 and t.category != TRANSFER


def balances(transactions: Iterable[Transaction]) -> dict[str, Decimal]:
    """The balance of each account, by account name, sorted by name."""
    totals = totals_by(transactions, key=lambda t: t.account)
    return dict(sorted(totals.items()))


def spending_by_category(transactions: Iterable[Transaction]) -> dict[str, Decimal]:
    """The spending of each category, as positive amounts, largest first."""
    spending = [t for t in transactions if is_spending(t)]
    totals = totals_by(spending, key=lambda t: t.category)
    return {c: -total for c, total in sorted(totals.items(), key=lambda item: item[1])}


def net_by_month(transactions: Iterable[Transaction]) -> dict[str, Decimal]:
    """Income minus spending of each month (`2026-01`...), sorted by month."""
    totals = totals_by(transactions, key=lambda t: t.date.strftime("%Y-%m"))
    return dict(sorted(totals.items()))
