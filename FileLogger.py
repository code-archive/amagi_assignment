#!/usr/bin/python3.6

import argparse
import os

parser = argparse.ArgumentParser(description="Interleaves log entries from different files as specified")
parser_group = parser.add_argument_group()
parser_group.add_argument('-n', '--number', dest="number_of_entries", type=str, help="Enter the number of entries "
                                                                                     "to be printed")
parser_group.add_argument('-l', '--lines', dest="number_of_lines", type=str, help="Enter the number of lines "
                                                                                     "to be picked")
parser_group.add_argument('-f', '--output', dest="output_file", type=str, help="Name of the output file ")
parser_group.add_argument('-t' ,'-total', dest = "total_files", type =str, help="Number of files to be picked")
parser_group.add_argument('-p', '--path', dest = 'folder_path', type =str, help= "Location of the folder to be used")

args = parser.parse_args()
if args.number_of_entries:
    number_of_entries = int(args.number_of_entries)
if args.number_of_lines:
    number_of_lines = int(args.number_of_lines)
if args.output_file:
    output_file_name =  args.output_file
if args.total_files:
    number_of_files = int(args.total_files)
if args.folder_path:
    file_path = args.folder_path


def add_into_file(line):
    """
    This method shall add the contents of line to file if they are not empty
    :param line: line entry
    :return: None
    """
    if len(line) != 0:
        with open(output_file_name, 'a') as fp:
            fp.writelines(line)


def get_specific_lines(file_name, start_line, num_of_lines):
    """
    This method gets lines specified number of lines from a file mentioned
    :param file_name: name of the input file to extract the lines from
    :param start_line: index of the starting line to be extracted
    :param num_of_lines: delta of lines to be extracted
    :return lines: List of lines extracted
    """
    with open(file_path+os.sep+file_name) as fp:
        lines = fp.readlines()[start_line:start_line + num_of_lines]
        return lines


#get_file_list
file_list = os.listdir(file_path)[0:number_of_files]
start_index = 0

while(number_of_entries):
    lines = []
    for file_name in file_list:
        lines = get_specific_lines(file_name, start_index, number_of_lines)
        add_into_file(lines)
    start_index = start_index+number_of_lines
    number_of_entries -= number_of_lines

    if not lines:
        break
