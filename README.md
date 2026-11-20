# smd-app

Personal finance ledger for the command line: balances, spending and monthly reports, stored in a SQLite database.

## Run it

    uv run ledger import
    uv run ledger balance
    uv run ledger spending
    uv run ledger months
    uv run ledger add checking -12.50 restaurants "Lunch"

## Roadmap

- A web API and a dashboard

## Author

victoring557

## Use of AI

I acknowledge the use of Grok (https://grok.com) to help with parts of Labs 6 and 7. The prompts used include "how do I split a Python script into a package with uv", "how do I define a foreign key and relationship in SQLAlchemy", "why does my import create duplicate rows" and "how to reject amounts with more than two decimals in Python". I used the answers as a starting point, then ran, checked and adapted the code myself.
