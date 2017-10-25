#!/usr/bin/env python

def type_check(correct_type):
    def check(old_function):
        def new_function(arg):
            if (isinstance(arg, correct_type)):
                return old_function(arg)
            else:
                print("From @type_check decorator, Value '%s' has bad type, should be %s" %(arg,str(correct_type)))
        return new_function
    return check

@type_check(int)
def times2(num):
    return num*2

input = 2
print("Result of times2(%s)=%s" %(input, times2(input)))

input = 'Not A Number'
print("Result of times2(%s)=%s" %(input, times2(input)))

@type_check(str)
def first_letter(word):
    return word[0]

input = 'Hello World'
print("Result of first_letter(%s)=%s" %(input, first_letter(input)))

input = ['Not', 'A', 'String']
print("Result of first_letter(%s)=%s" %(input, first_letter(input)))
