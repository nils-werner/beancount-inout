#!/usr/bin/env python

import sys
from datetime import datetime, date
from decimal import Decimal

import click
from beancount.core import data, flags, amount
from beancount.parser import printer

@click.command()
@click.option('-i', '--income', help="The income (debited) account", default="Income:Work")
@click.option('-p', '--payee', help="Payee line")
@click.option('-s', '--subject', help="Subject line")
@click.option('-r', '--rate', help="Hourly rate in 'units currency'")
@click.option('-u', '--unit', help="Work unit", default="WKHR")
@click.option('-h', '--hours', help="Hours spent working", type=float)
@click.argument('asset')
def inout(income, payee, subject, rate, unit, hours, asset):
    starttime = datetime.now()

    if subject is None:
        subject = click.prompt('Subject', default="", err=True)

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
            click.confirm('Finish work', default=True, err=True)
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

    printer.print_entry(txn)
