#!/usr/bin/env python3

import functools
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


@functools.cache
def distance_squared(a: CoordType, b: CoordType) -> int:
    """As we're only comparing distances, and we don't need the actual distance, we don't need to do the final sqrt."""
    return sum((xa - xb) ** 2 for xa, xb in zip(a, b, strict=True))


def part1(input_data: InputType, num_connections: int = 1000) -> ResultType:
    circuits: set[frozenset[CoordType]] = {frozenset({coord}) for coord in input_data}

    for a, b in itertools.islice(sorted(itertools.combinations(input_data, 2), key=lambda t: distance_squared(t[0], t[1])), num_connections):
        # Merge circuits containing a and b, if not already part of the same circuit.
        circuit_a = {c for c in circuits if a in c}.pop()
        circuit_b = {c for c in circuits if b in c}.pop()
        if circuit_a != circuit_b:
            circuits = {c for c in circuits if a not in c and b not in c} | {circuit_a | circuit_b}

    return math.prod(itertools.islice(sorted((len(circuit) for circuit in circuits), reverse=True), 3))


def part2(input_data: InputType) -> ResultType:
    circuits: set[frozenset[CoordType]] = {frozenset({coord}) for coord in input_data}

    @functools.cache
    def min_distance_squared(circuit_a: frozenset[CoordType], circuit_b: frozenset[CoordType]) -> int:
        """Find the square of the distance between the closest junction boxes in two circuits."""
        return min(distance_squared(a, b) for a, b in itertools.product(circuit_a, circuit_b))

    while len(circuits) > 2:
        circuit_a, circuit_b = min(((circuit_a, circuit_b) for circuit_a, circuit_b in itertools.combinations(circuits, 2)), key=lambda t: min_distance_squared(*t))
        circuits = (circuits - {circuit_a, circuit_b}) | {(circuit_a | circuit_b)}

    final_a, final_b = min(((a, b) for a, b in itertools.product(*circuits)), key=lambda t: sum((x - y) ** 2 for x, y in zip(*t, strict=True)))
    return final_a[0] * final_b[0]
