#!/usr/bin/env python

import sys
from datetime import datetime, date
from decimal import Decimal
from contextlib import contextmanager

import click
from beancount.core import data, flags, amount
from beancount.parser import printer


# Do this because of
# https://github.com/pallets/click/issues/2018
@contextmanager
def to_stderr():
    sys.stdout = sys.__stderr__
    yield
    sys.stdout = sys.__stdout__


@click.command()
@click.option('-i', '--income', help="The income (debited) account", default="Income:Work", show_default=True)
@click.option('-p', '--payee', help="Payee line")
@click.option('-s', '--subject', help="Subject line")
@click.option('-r', '--rate', help="Hourly rate in units and currency, e.g. '60 USD'")
@click.option('-u', '--unit', help="Work unit", default="WKHR", show_default=True)
@click.option('-h', '--hours', help="Hours spent working", type=float)
@click.argument('asset')
def inout(income, payee, subject, rate, unit, hours, asset):
    starttime = datetime.now()

    if subject is None:
        with to_stderr():
            subject = click.prompt('Subject', default="", err=False)

    txn = data.Transaction(
        date=date.today(),
        meta=None,
        tags=None,
        links=None,
        flag=flags.FLAG_OKAY,
        payee=payee,
        narration=subject,
        postings=[],
    )

    if hours is None:
        try:
            with to_stderr():
                click.confirm('Finish work', default=True, err=False)
        except KeyboardInterrupt:
            sys.exit(1)

    endtime = datetime.now()

    difference = endtime - starttime

    if hours is None:
        hours = difference.seconds / 3600

    hours = Decimal(hours)
    hours = hours.quantize(Decimal('.001'))

    if rate is not None:
        rate = amount.from_string(rate)

    txn.postings.append(
        data.Posting(
            asset,
            amount.Amount(hours, unit),
            None,
            rate, None, None
        )
    )
    txn.postings.append(
        data.Posting(
            income, None, None, None, None, None
        )
    )

    # Do this to print line before, not after
    out = printer.format_entry(txn).strip()
    print()
    print(out)
