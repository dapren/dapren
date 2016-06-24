__author__ = 'dapren'

from __future__ import print_function
"""
This python code kinda implements the toString() of data structures
"""


def echo(any_object):
    if type(any_object) is list:
        for item in any_object:
            print (item, sep="\n")