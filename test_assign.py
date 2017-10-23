#!/usr/bin/env python

import os
import sys
import csv
import collections

x = [1, 2, 3]
y = x
print(x) # [1, 2, 3]
y += [3, 2, 1]
print(x) # [1, 2, 3, 3, 2, 1]
print(y) # [1, 2, 3, 3, 2, 1]

sys.exit()

def read_delimited_file(filename, delimiter):
    """ Read the contents of a csv file into a 2D array, ignoring comment fields """
    ary = list()
    f = open(filename,"r")
    rlines = csv.reader(f, delimiter=delimiter)
    for row in rlines:
        if row[0][0] == "#":
            continue
        cary = list()
        for col in row:
            if col[0] != "#":
                cary.append(col)
        if cary:
            ary.append(cary)
    f.close()
    return ary


def format_array(arry):
    delim = ","
    string = ""
    for row in arry:
        for col in row:
            string += col + delim
        string = string[:len(string)-1] + "\n"
    return string

myfile = "Downloads/edstocks20170803.txt"
arry = read_delimited_file(myfile,"\t")
#print("file("+myfile+")=\n"+format_array(arry))

name = "hello, there"
if "," in name:
    print("There is a comma in name")
if "ll" in name:
    print("There is a ll in name")
if "lala" in name:
    print("There is a ll in name")
else:
    print("There is not a lala in name")

name = "LastPrice"
if "PRICE" in name.upper():
    print("There is a PRICE in upper name")
if "PRICE" in name:
    print("There is not a PRICE in name")


import logging
logger = logging.getLogger(__name__)
try:
    raise Exception("abc","ok")
except Exception as e:
    print(e)
    print(e.args)
    logger.error(e)
    #raise

class Simple(object):
    def method1(self, arg="no arg"):
        print("method1 no arg=%s" % arg)
        pass
    def method2(self, arg):
        print("method1 no arg=%s" % arg)
        self.method1("yes2")
        raise Exception();

s = Simple()
s.method1()
s.method1("yes")

print("Goodbye")
