#!/usr/bin/python3.6

import argparse

parser = argparse.ArgumentParser(description="Generate Fibonacci numbers which are in odd positions")
parser_group = parser.add_argument_group()
parser_group.add_argument('-n', '--number', dest="number_of_entries", type=str, help="Enter the number of entries "
                                                                                     "to be printed")

args = parser.parse_args()
if args.number_of_entries:
    number = int(args.number_of_entries)

fibn = 0    # Fibinocci n
fibnp1 = 1  # Fibinocci n+1
print (fibnp1)
while (number):
    #reiterate fibonacci generation twice to skip the even positions.
    fibnp1= fibnp1+ fibn
    fibn= fibnp1 - fibn

    fibnp1= fibnp1+ fibn
    fibn = fibnp1 - fibn

    print(fibnp1)
    number -=1



