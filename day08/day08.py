#!/usr/bin/env python3

import itertools
import math
from pathlib import Path

CoordType = tuple[int, int, int]
InputType = list[CoordType]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        result = [tuple([int(part) for part in line.strip().split(",")]) for line in f.readlines()]
    assert all([len(coord) == 3 for coord in result])
    return result


def part1(input_data: InputType, num_connections: int = 1000) -> ResultType:
    circuits: set[frozenset[CoordType]] = {frozenset({coord}) for coord in input_data}

    # As we're only comparing distances, we don't need to do the final sqrt.
    def distance_squared(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
        return sum((xa - xb) ** 2 for xa, xb in zip(a, b, strict=True))

    for a, b in itertools.islice(sorted(itertools.combinations(input_data, 2), key=lambda t: distance_squared(t[0], t[1])), num_connections):
        # Merge circuits containing a and b, if not already part of the same circuit.
        circuit_a = {c for c in circuits if a in c}.pop()
        circuit_b = {c for c in circuits if b in c}.pop()
        if circuit_a != circuit_b:
            circuits = {c for c in circuits if a not in c and b not in c} | {circuit_a | circuit_b}

    return math.prod(itertools.islice(sorted((len(circuit) for circuit in circuits), reverse=True), 3))


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
