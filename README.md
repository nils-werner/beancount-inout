# Beancount Inout

## Time tracking for beancount

Beancount is exceptionally well equipped to do time tracking, all it is missing is a convenient "in/out" tool. `bean-inout` provides this tool.

## Example Output

```sh
$ bean-inout Assets:DE:Employer:Work
Subject []:                           # enter an optional subject line, while you work
Finish work [Y/n]:                    # press return 2 hours later
```

returns

```
2021-07-27 *
  Assets:DE:Employer:Work  2 WKHR
  Income:Work
```

To automatically append the returned data to your work ledger, simply redirect it into the file

```sh
$ bean-inout Assets:DE:Employer:Work >> work.bean
```

## Parameters

`bean-inout` provides a lot of parameters to configure most data in the entries, including subject lines, work rates, hours worked etc.:

```
Usage: bean-inout [OPTIONS] ASSET

Options:
  -i, --income TEXT   The income (debited) account
  -p, --payee TEXT    Payee line
  -s, --subject TEXT  Subject line
  -r, --rate TEXT     Hourly rate in 'units currency'
  -u, --unit TEXT     Work unit
  -h, --hours FLOAT   Hours spent working
  --help              Show this message and exit.
```

For example

```
$ bean-inout \
  -i Income:Freelance-Work \
  -p "Client 1" \
  -s "Workpackage 1" \
  -r "100 USD" \
  -u WORKHR \
  -h 1 Asset:DE:Client-One:Project-One
```

results in an entry

```
2021-07-27 * "Client 1" "Workpackage 1"
  Asset:DE:Client-One:Project-One  1.000 WORKHR @ 100 USD
  Income:Freelance-Work
```
