from __future__ import print_function
from lib.fileops import file2list
import argparse
from argparse import RawTextHelpFormatter


def process(filename, func, bracket_start, bracket_end):
	str = "\n".join(file2list(filename))

	bracket_open = 0

	str = str.replace('(', ' ( ')\
				.replace(')', ' ) ')\
				.replace(']', ' ] ')\
				.replace('[', ' [ ')

	in_func = False

	for word in str.split(" "):
		if word.find(func) > -1:
			in_func = True
			continue

		if in_func == True:
			if word == bracket_start:
				bracket_open += 1
				continue
			elif word == bracket_end:
				bracket_open -= 1
				continue
		else:
			continue

		if bracket_open > 0:
			print (word, end=" ")
		else:
			in_func = False


def process_command_line_args():
    global args

    epilog = """
"""

    parser = argparse.ArgumentParser(description='Extract key value parameter from a python function ',
                                     formatter_class=RawTextHelpFormatter,
                                     epilog=epilog)

    parser.add_argument('filename',
                        help='Absolute location of file')

    parser.add_argument('func',
                        help='Name of function')

    parser.add_argument('bracket_start',
                        help='Bracket start type, (, [, {')

    parser.add_argument('bracket_end',
                        help='Bracket end type, ],},)')

    args = parser.parse_args()


if __name__ == '__main__':
    process_command_line_args()
    process(
		args.filename,
		args.func,
		args.bracket_start,
		args.bracket_end
	)





