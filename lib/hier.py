from __future__ import print_function
import sys
from collections import deque

"""
This script reads from stdin a tab delimited stream with 2 fields
    1. Process
    2. Depends On Process
and outputs the upsteam and downstream process for each process

Example input:
p3  p2
p2  p1
p3  p1
p3  p4
p5  p3

The above input can be read as
"process p3 depends on process p2"
"process p2 depends on process p1"
and so on

then the output will be
p1	p2	downstream
p1	p3	downstream
p1	p5	downstream
p2	p1	upstream
p2	p3	downstream
p2	p5	downstream
p3	p1	upstream
p3	p2	upstream
p3	p4	upstream
p3	p5	downstream
p4	p3	downstream
p4	p5	downstream
p5	p1	upstream
p5	p2	upstream
p5	p3	upstream
p5	p4	upstream
"""
global dep_upstream_map
dep_upstream_map = {}

global dep_downstream_map
dep_downstream_map = {}


def create_map(input_line):
    process, upstream_process = input_line.split("\t")

    # Prepare map for upstream calculations
    if process in dep_upstream_map:
        dep_list = dep_upstream_map.get(process)
        dep_list.append(upstream_process)
        dep_upstream_map[process] = dep_list
    else:
        dep_list = [upstream_process]
        dep_upstream_map[process] = dep_list

    # Prepare map for downstream calculations
    downstream_process, process = input_line.split("\t")
    if process in dep_downstream_map:
        dep_list = dep_downstream_map.get(process)
        dep_list.append(downstream_process)
        dep_downstream_map[process] = dep_list
    else:
        dep_list = [downstream_process]
        dep_downstream_map[process] = dep_list


def create_hier(hier_type, dep_map):
    for process in dep_map.keys():
        process_list = []
        dep_list = deque(dep_map.get(process))

        while len(dep_list) > 0:
            dep_process = dep_list.pop()
            process_list.append(dep_process)

            if dep_map.get(dep_process) is not None:
                for more_process in dep_map.get(dep_process):
                    if more_process not in process_list:
                        dep_list.appendleft(more_process)

        final_upstream_list = sorted(set(process_list))
        for dep_process in final_upstream_list:
            print ("{0}\t{1}\t{2}".format(process, dep_process, hier_type))

for line in sys.stdin:
    line = line.strip()
    create_map(line)

create_hier("upstream", dep_upstream_map)
create_hier("downstream", dep_downstream_map)



