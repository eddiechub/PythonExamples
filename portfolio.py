#!/usr/bin/env python

import unittest 
import sys, os
import csv
import requests
import collections
from decimal import Decimal

__any__  = [
    'portfolio',
    'portfolio.Portfolio',
    'portfolio.Portfolio.name',
]

class Instrument:
    """ Class: Instrument
    """

    type = "Instrument"

    def __init__(self, name):
        self.name = name
        self.values = {}

    @property
    def add_values(self, values):
        """ Should be a collection """
        self.values = values

    def get_values(self):
        return self.values

    def get_field(self, field):
        try:
            return self.values[field]
        except KeyError as e: 
            raise

    def set_field(self, field, data):
        self.values[field] = data

    def generate_request_symbol(self):
        if "=" in self.name:
            print("%s is a FX" % self.name)


class Portfolio:
    """ Portfolio - manage portfolio contents
    """

    ctype = "Portfolio"
    __name = 'Portfolio Class Name'

    def __init__(self, name):
        self._name = name
        self._financial_instruments = collections.OrderedDict()

    @staticmethod
    def sname():
        return "You know it baby!"

    @classmethod
    def classrepr(cls):
        return repr(cls)

    @classmethod
    def clsname(cls):
        return cls.__name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def add_instrument(self, name, instrument):
        self._financial_instruments[name] = instrument

    def get_instrument(self, name):
        return self._financial_instruments[name]

    def show_instruments(self):
        for name, instrument in self._financial_instruments.items():
            if isinstance(instrument, Instrument):
                val = instrument.get_field("init_value")
                print("name: %s init_value: %s" % (name, val))
                field_values = instrument.get_values()
                for field, value in field_values.items():
                    print("name: %s field: %s value: %s" % (name, field, value))

            else:
                print("name: %s value: %s" % (name, type(values)))

    def read_instrument_file(self, filename, delimiter):
        """ Read the contents of a csv file into a 2D array, ignoring comment fields """
        f = open(filename,"r")
        rlines = csv.reader(f, delimiter=delimiter)
        for row in rlines:
            if row[0][0] == "#" or len(row) < 3:
                continue
            name = row[0]
            instrument = Instrument(name)
            if not instrument:
                print("Instrument -- what??")
                raise
            #print("%s: init_value=%s" % (name, row[1]))
            instrument.set_field("init_value", row[1])
            instrument.set_field("amount1", row[2])
            instrument.set_field("amount2", row[3])
            self.add_instrument(name, instrument)

            if name == "CASH":
                self.cash1 = float(row[2])
                self.cash2 = float(row[3])

        f.close()

    def readPortfolio(self, myfile):
        self.read_instrument_file(myfile,"\t")

    def derive_ticker(self, name):

        tickerLen = len(name)
        if name == "CASH":
            ticker = None
        else:
            ticker = name

        pos = name.find(".")
        if pos == 0:
            ticker = '^' + name[1:] 

        elif name[tickerLen-1] == '=':
            # ignore for now
            # ticker =~ s/^(\w+)=$/${1}USD=/ if $record =~ /EUR|GBP/;
            # ticker .= "X";
            pass

        if name == "^SPX":
            ticker = "^GSPC"
        elif ticker == "^DJI":
            # use the ETF which is around 100x less than dow
            ticker = "DIA"
            #ticker = "INDU"
        elif "c1" in name:
            # ignore futures prices for now
            pass

        if pos > 0:
            ticker = name[0:pos]

        # Map the string to name
        self.ticker_map[ticker] = name

        if ticker != name:
            #print("converted %s to %s" % (name, ticker));
            pass

        return ticker

    def get_tickers(self):
        self.ticker_map = {}
        ticker_list = list()
        for name in self._financial_instruments.keys():
            ticker = self.derive_ticker(name)
            if ticker:
                ticker_list.append(ticker)

        # convert to comma list
        ticker_string = ",".join(ticker_list)
        return ticker_string

    def get_name(self, ticker):
        return self.ticker_map[ticker]

    def processResponse(self, res):
        r = csv.reader(res.splitlines(), delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        for row in r:
            #print("line=%s" % row)
            #for col in row:
            #    print("col=%s" % col)
            if len(row) < 3:
                continue

            ticker = row[0]

            if row[3] == "N/A":
                row[3] = "0"
            if row[5] == "N/A":
                row[5] = "0"
            if row[6] == "N/A":
                row[6] = "0"
            if row[7] == "N/A":
                row[7] = "0"
            if row[8] == "N/A":
                row[8] = "0"

            name = self.get_name(ticker)
            desc = row[1]
            if desc == "N/A":
                continue;
            #print("%s: %s" %(ticker,name))

            instrument = self._financial_instruments[name]
            instrument.set_field("description", row[1])
            instrument.set_field("last", row[2])
            instrument.set_field("change", row[3])
            instrument.set_field("volume", row[4])
            instrument.set_field("yrhigh", row[5])
            instrument.set_field("yrlow", row[6])
            instrument.set_field("high", row[7])
            instrument.set_field("low", row[8])
            instrument.set_field("prev", row[9])

    def print_values(self):
        for name, instrument_values in self._financial_instruments.items():
            try:
                init_val = instrument_values.get_field("init_value")
                a1 = instrument_values.get_field("amount1")
                a2 = instrument_values.get_field("amount2")
                desc = instrument_values.get_field("description")
                last = instrument_values.get_field("last")
            except KeyError as e: 
                continue

            print("{desc}: {cost} {a1} {a2} {last}".format(desc=desc, cost=init_val, a1=a1, a2=a2, last=last))

    def print_format(self):
        # Will be set or derived
        doWide = True
        hasMultipleQuantity = True

        header = " Name                Last  YrHigh   YrLow  "
        if doWide:
            header += "  High     Low  Change     Volume  "
        else:
            header += "Change  "

        if hasMultipleQuantity:
            header += "  Sub1    Sub2   Total DayPNL"
        else:
            header += " Total DayPNL"

        if doWide:
            header += "    PNL"

        print(header)

        total1 = self.cash1
        total2 = self.cash2;
        total = total1 + total2;
        total_change = 0.0;
        total_pnl = 0.0;
        cash1 = 0.0;
        cash2 = 0.0;

        for name, instrument_values in self._financial_instruments.items():
            try:
                purch = float(instrument_values.get_field("init_value"))
                quantity1 = float(instrument_values.get_field("amount1"))
                quantity2 = float(instrument_values.get_field("amount2"))
                desc = instrument_values.get_field("description")
                last = float(instrument_values.get_field("last"))
                change = float(instrument_values.get_field("change"))
                volume = int(instrument_values.get_field("volume"))
                yrhigh = float(instrument_values.get_field("yrhigh"))
                yrlow = float(instrument_values.get_field("yrlow"))
                high = float(instrument_values.get_field("high"))
                low = float(instrument_values.get_field("low"))
                prev = float(instrument_values.get_field("prev"))
            except KeyError as e: 
                continue

            sub1 = quantity1 * last;
            sub2 = quantity2 * last;
            subtotal = sub1 + sub2;
            subtotal_change = 0 + change * (quantity1 + quantity2);
            subtotal_pnl = subtotal - purch;
            total_change += subtotal_change;

            total1 += sub1;
            total2 += sub2;
            total += subtotal;
            total_pnl += subtotal_pnl;

            lformat = "7.3f"
            if last >= 10000:
                lformat = "7.1f"
            elif last >= 1000:
                lformat = "7.2f"

            yhformat ="7.3f"
            if yrhigh >= 10000:
                yhformat = "7.1f"
            elif yrhigh >= 1000:
                yhformat = "7.2f"

            ylformat = "7.3f";
            if yrlow >= 10000:
                ylformat = "7.1f"
            elif yrlow >= 1000:
                ylformat = "7.2f"

            hformat = "7.3f"
            if high >= 10000:
                hformat = "7.1f"
            elif high >= 1000:
                hformat = "7.2f"

            loformat = "7.3f"
            if low >= 10000:
                loformat = "7.1f"
            elif low >= 1000:
                loformat = "7.2f"

            cformat = "7.3f"
            if change >= 10000 or change <= -1000:
                cformat = "7.1f"
            elif change >= 1000 or change <= -100:
                cformat = "7.2f"

            if last == 0.0 and prev != 0.0:
                last = prev

            if name == "GCc1":
                name = "GOLD! "

            if name == "NY RBOB":
                name = "UNLEAD GAS"

            if doWide:
                if hasMultipleQuantity:
                    fstr = " {desc:16s} {last:"+lformat+"} {yrhigh:"+yhformat+"} {yrlow:"+ylformat+"} {high:"+hformat+"} {low:"+loformat+"} {change:"+cformat+"} {volume:10d} {sub1:7.0f} {sub2:7.0f} {subtotal:7.0f} {subtotal_change:6.0f} {subtotal_pnl:6.0f}"
                    print(fstr.format(
                        desc=desc[:16],
                        last=last,
                        yrhigh=yrhigh, yrlow=yrlow, high=high, low=low,
                        change=change, volume=volume, sub1=sub1, sub2=sub2,
                        subtotal=subtotal, subtotal_change=subtotal_change, subtotal_pnl=subtotal_pnl
                        ))

        if doWide:
            if hasMultipleQuantity:
                instrument_values = self._financial_instruments["CASH"]
                if instrument_values:
                    cash1 = float(instrument_values.get_field("amount1"))
                    cash2 = float(instrument_values.get_field("amount2"))

                if cash1 > 0 or cash2 > 0:
                    print(" CASH {cash1:78d} {cash2:7d} {cashtot:7d}".format(cash1=int(cash1), cash2=int(cash2), cashtot=int(cash1 + cash2)))

                print(" TOTALS{total1:77.0f} {total2:7.0f} {total:7.0f} {total_change:6.0f} {total_pnl:6.0f}".format(
                    total1=total1,
                    total2=total2,
                    total=total,
                    total_change=total_change,
                    total_pnl=total_pnl
                    ))

    def test_derive_ticker(self):
        name = "DD.N"
        name = ".SPX"
        name = ".DJI"
        print("name=%s ticker=%s" % (name, derive_ticker(name)))

    def get_data(self, symlist = "GOOG"):
        yformat = "snl1c1vkjhgpw";
        url = "http://download.finance.yahoo.com/d/quotes.csv?s={symlist}&f={yformat}&e=.csv".format(symlist=symlist,yformat=yformat);
        r = requests.get(url)
        if r.status_code == 403:
            print(r.text)
            # Should throw
            return ""

        response = ""
        for line in r:
            if isinstance(line,bytes):
                response += line.decode('utf-8')
            else:
                response += line

        # print(response)

        #print('\nDisplay all headers\n')
        #print(r.headers)

        return response

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        pass
        #print("SetUp")

    def tearDown(self):
        pass
        #print("Teardown")

    def doCleanups(self):
        pass
        #print("doCleanups")

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_instrunment(self):
        instrument = Instrument("EUR=")

        from unittest import mock
        instrument.generate_request_symbol = mock.Mock()
        instrument.generate_request_symbol()

        self.assertTrue(instrument)
        #print("%s: init_value=%s" % (name, row[1]))
        instrument.set_field("init_value", 100)
        instrument.set_field("amount1", 10)
        instrument.set_field("amount2", 20)
        self.assertEqual(instrument.get_field("amount2"),20.090)

if __name__ == "__main__":
    unittest.main()

"""
import urllib.request
def meth1():
    source = "http://stackoverflow.com"
    f = urllib.request.urlopen("http://stackoverflow.com")
    print(f.read())
"""
