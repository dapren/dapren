__author__ = 'dapren'

from __future__ import print_function
"""
This python code kinda implements the toString() of data structures
"""
def echo(object):
    if type(object) is list:
        for item in object:
            print (item, sep="\n")