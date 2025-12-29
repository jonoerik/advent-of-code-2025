#!/usr/bin/env python3

import functools
import operator
from pathlib import Path

InputType = dict[str, set[str]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return {k: vs.split() for k, vs in (line.split(": ", 2) for line in f.readlines())}


def topological_sort(input_data: InputType) -> list[str]:
    # Topologically sort nodes using Kahn's algorithm.
    nodes = set(input_data.keys()) | functools.reduce(operator.or_, (set(l) for l in input_data.values()), set())

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
    return sorted_nodes


def count_paths(input_data: InputType, sorted_nodes: list[str], source_node: str, dest_node: str) -> int:
    # Number of paths from node n to dest is the sum of the numbers of paths from each of n's
    # children to dest.
    paths_to_dest: dict[str, int] = {dest_node: 1}
    for n in reversed(sorted_nodes[sorted_nodes.index(source_node):sorted_nodes.index(dest_node)]):
        paths_to_dest[n] = sum(paths_to_dest[m] if m in paths_to_dest.keys() else 0 for m in input_data[n])

    return paths_to_dest[source_node]


def part1(input_data: InputType) -> ResultType:
    sorted_nodes = topological_sort(input_data)
    return count_paths(input_data, sorted_nodes, "you", "out")


def part2(input_data: InputType) -> ResultType:
    sorted_nodes = topological_sort(input_data)
    # The earlier of the 2 intermediate required nodes in the topological sort must
    # be visited before the latter, so we don't need to check both orderings.
    a, b = ("dac", "fft") if (sorted_nodes.index("dac") < sorted_nodes.index("fft")) else ("fft", "dac")
    return (count_paths(input_data, sorted_nodes, "svr", a) *
            count_paths(input_data, sorted_nodes, a, b) *
            count_paths(input_data, sorted_nodes, b, "out"))
