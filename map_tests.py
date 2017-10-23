#!/usr/bin/env python

org_text = "Use capitalize_all to write a function named capitalize_nested that takes a nested list of strings and returns a new nested list with all strings capitalized"

test_list = org_text.split()
new_list = [word.capitalize() for word in test_list]

new_text = " ".join(new_list)

print(org_text)
print(new_text)

