#!/usr/bin/env python

import sys
from datetime import datetime, date
from decimal import Decimal

from beancount.core import data, flags, amount
from beancount.parser import printer

income = sys.argv[1]
asset = sys.argv[2]
try:
    payee = sys.argv[3]
except IndexError:
    payee = ""
try:
    narration = sys.argv[4]
except IndexError:
    narration = ""

txn = data.Transaction(
    date=date.today(),
    meta=None,
    tags=None,
    links=None,
    flag=flags.FLAG_OKAY,
    payee=payee,
    narration=narration,
    postings=[],
)

starttime = datetime.now()

try:
    _ = input()
except EOFError:
    pass
except KeyboardInterrupt:
    sys.exit(1)

endtime = datetime.now()

difference = endtime - starttime
hours = Decimal(difference.seconds / 36)
hours = hours.quantize(Decimal('.001'))

txn.postings.append(
    data.Posting(
        asset,
        amount.Amount(hours, 'WKHR'),
        None, None, None, None
    )
)
txn.postings.append(
    data.Posting(
        income, None, None, None, None, None
    )
)

printer.print_entry(txn)
