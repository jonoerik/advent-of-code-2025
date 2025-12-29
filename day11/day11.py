#!/usr/bin/env python3

import functools
import operator
from pathlib import Path

InputType = dict[str, set[str]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return {k: vs.split() for k, vs in (line.split(": ", 2) for line in f.readlines())}


def part1(input_data: InputType) -> ResultType:
    # Count the number of distinct paths from 'you' to 'out'.
    nodes = set(input_data.keys()) | functools.reduce(operator.or_, (set(l) for l in input_data.values()), set())

    # Topologically sort nodes using Kahn's algorithm.
    sorted_nodes = []
    current_set = {n for n in nodes if not any(n in v for v in input_data.values())}
    while current_set:
        n = current_set.pop()
        sorted_nodes.append(n)
        if n in input_data.keys():
            for m in input_data[n]:
                if not any(m in v for k, v in input_data.items() if k not in sorted_nodes and k != m):
                    current_set.add(m)

    assert len(sorted_nodes) == len(nodes)
    # Remove nodes not between "you" and "out", and remove out itself.
    sorted_nodes = sorted_nodes[sorted_nodes.index("you"):sorted_nodes.index("out")]

    # Number of paths from node n to out is the sum of the numbers of paths from n's
    # children to out.
    paths_to_out: dict[str, int] = {"out": 1}
    for n in reversed(sorted_nodes):
        paths_to_out[n] = sum(paths_to_out[m] for m in input_data[n])

    return paths_to_out["you"]


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
