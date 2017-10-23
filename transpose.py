#!/usr/bin/env python

import sys
import csv

array = [['A',2,3],['B',4,5],['C',6,7]]

num_rows = len(array)
num_cols = len(array[0])

print("Here is the original matrix")
rary = []
for row in range(num_rows):
	cary = []
	for col in range(len(array[row])):
		print(array[row][col],end=' ')
		cary.append(array[row][col])
	print("")
	rary.append(cary)

print("Here is the transposed matrix")
for col in range(num_cols):
	for row in range(len(rary)):
		cary = rary[row]
		print(cary[col],end=' ')
	print("")


print("Readubf matrix")
f = open("matrix.txt","r")
r = csv.reader(f)
num_rows = 0;
num_cols = 0;
row_list = list()
for row in r:
    col_list = list()
    for col in row:
        col_list.append(col.strip())
    row_list.append(col_list)
    if len(col_list) > num_cols:
        num_cols = len(col_list)
f.close()

num_rows = len(row_list)

print("Number of columns=%d" % num_cols)
print("Number of rows=%d" % num_rows)
for col in range(num_cols):
    for row in range(num_rows):
        cary = rary[row]
        print(cary[col],end=' ')
    print("")


