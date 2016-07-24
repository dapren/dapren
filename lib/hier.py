from __future__ import print_function

import sys
from collections import deque

global dep_map
dep_map = {}


def create_map(input_line):
    process, upstream_process = input_line.split("\t")
    
    if process in dep_map:
        dep_list = dep_map.get(process)
        dep_list.append(upstream_process)
        dep_map[process] = dep_list
    else:
        dep_list = [upstream_process]
        dep_map[process] = dep_list


def create_upstream():

    for process in dep_map.keys():
        print (process)
        upstream_process_list = []
        dep_list = deque(dep_map.get(process))

        while len(dep_list) > 0:
            upstream_process = dep_list.pop()
            upstream_process_list.append(upstream_process)

            if dep_map.get(upstream_process) is not None:
                for i in dep_map.get(upstream_process):
                    if i not in upstream_process_list:
                        dep_list.appendleft(i)

        print (sorted(set(upstream_process_list)))

for line in sys.stdin:
    line = line.strip()
    create_map(line)

create_upstream()



