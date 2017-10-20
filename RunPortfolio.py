#!/usr/bin/env python
import os
import sys
import csv
import argparse
import collections
import portfolio 
#import portfolio.Portfolio
#from portfolio import Portfolio
from datetime import datetime as dt
#print(dir(portfolio))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get Portfolio Prices - Process Arguments', epilog="ok, so you're getting closer")
    parser.add_argument('-v', '--verbose', dest="verbose", action='count', help='Add Verbosity')
    parser.add_argument('-f', '--file', nargs="?", dest="myfile", action='store', default="edstocks20171015.txt", help='portfolio filename')
    args = parser.parse_args()

    if not os.path.isfile(args.myfile):
        args.myfile = "Downloads/"+args.myfile

    if os.path.isfile(args.myfile):

        edsport = portfolio.Portfolio("EdsList")
        if args.verbose:
            print("ClassType=%s StaticName=%s ClassName=%s ClassRepr=%s Portfolio Name=%s" %
                (portfolio.Portfolio.ctype,
                portfolio.Portfolio.sname(),
                edsport.clsname(),
                edsport.classrepr(),
                edsport.name))

        print("File: [%s] Time: [%s] Source: Yahoo Finance" % (args.myfile, dt.ctime(dt.today())))
        edsport.readPortfolio(args.myfile)

        #edsport.add_instrument("IBM",1)
        #edsport.add_instrument("FF",2)
        #edsport.show_instruments()

        tickers = edsport.get_tickers()
        #print(tickers)

        res = edsport.get_data(tickers)
        edsport.processResponse(res)

        #edsport.print_values()
        edsport.print_format()

    else:
        print("Cannot open file="+args.myfile)

#print("Goodbye")
