#!/usr/bin/env python

input_str1 = raw_input()
input_str2 = raw_input()

x1, y1, r1 = input_str1.split()
x2, y2, r2 = input_str2.split()

ix1, iy1, ir1 = int(x1), int(y1), int(r1)
ix2, iy2, ir2 = int(x2), int(y2), int(r2)

#print "x1=%d y1=%d r1=%d" % (ix1, iy1, ir1)
#print "x2=%d y2=%d r2=%d" % (ix2, iy2, ir2)

xd = ix1-ix2
yd = iy1-iy2
dis1 = (xd ** 2 + yd ** 2)
dis = (xd ** 2 + yd ** 2) ** (1.0/2.0)

total_rad = ir1 + ir2

#print "dis1=%d 1dis=%d totalrad=%d" %(dis1,dis,total_rad)

if total_rad > dis:
    print "YES"
else:
    print "NO"
