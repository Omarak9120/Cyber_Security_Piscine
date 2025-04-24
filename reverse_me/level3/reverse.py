#!/usr/bin/python3

s = "********"
omar = "42"

index = 3
for i in range(1, len(s)):
	print(f's[{i}]: {s[i]} {ord(s[i])}')
	omar = omar + f'{ord(s[i]):0>3}'

print("Result:", omar)