#!/usr/bin/env python

input_str = ""
m = 0
while input_str is not None:
  try:
    # py2
    input_str = raw_input()
    # py3
    #input_str = input()
    m += int(input_str)
  except:
    input_str = None
print(m)
