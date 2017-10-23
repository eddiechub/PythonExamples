#!/usr/bin/env python


def are_sets_permutive(set1, set2):

    # so we don't mess up the original mutables
    i1 = sorted(set1)
    i2 = sorted(set2)
    #print("p:i1=%s" % i1)
    #print("p:i2=%s" % i2)
    return i1 == i2


def are_sets_reversed(set1, set2):

    # we know they are permutive
    #i1 = set1.copy()
    i1 = set1[:]
    #i2 = sorted(set2, reverse=True)
    i2 = set2[::-1]
    #print("r:i1=%s" % i1)
    #print("r:i2=%s" % i2)

    if i1 != i2:
        i1 = set1[::-1]
        #i2 = set2.copy()
        i2 = set2[:]

    return i1 == i2


set1 = [1,2,3,4,5,6,7,8,9,10,11]
set2 = [2,1,4,3,5,6,7,8,9,10,11]
set3 = [2,1,4,3,5,6,7,8,9,10,99]
set4 = [11,10,9,8,7,6,5,4,3,2,1]

#print("sorted set1=%s" % sorted(set1))
#print("sorted set2=%s" % sorted(set2))
#set3.sort() # mutilates the original
#print("sorted set3=%s" % set3)

if are_sets_permutive(set1, set2):
    print("set 1 and 2 are permutive")
    if are_sets_reversed(set1, set2):
        print("set 1 and 2 are reversed")
else:
    print("set 1 and 2 are not permutive")

#print("set1=%s" % set1)
#print("set2=%s" % set2)

if are_sets_permutive(set1, set3):
    print("set 1 and 3 are permutive")
    if are_sets_reversed(set1, set3):
        print("set 1 and 3 are reversed")
else:
    print("set 1 and 3 are not permutive")

#print("set1=%s" % set1)
#print("set3=%s" % set3)

if are_sets_permutive(set1, set4):
    print("set 1 and 4 are permutive")
    if are_sets_reversed(set1, set4):
        print("set 1 and 4 are reversed")
else:
    print("set 1 and 4 are not permutive")

#print("set1=%s" % set1)
#print("set4=%s" % set4)
