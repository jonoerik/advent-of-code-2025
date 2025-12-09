#!/usr/bin/env python3

import itertools
import math
from pathlib import Path

InputType = list[tuple[int, int]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        result = [tuple(int(x) for x in line.strip().split(",")) for line in f.readlines()]
    assert all(len(coord) == 2 for coord in result)
    return result


def part1(input_data: InputType) -> ResultType:
    return max(math.prod(abs(x - y + 1)
                         for x, y in zip(a, b, strict=True))
               for a, b in itertools.combinations(input_data, 2))


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
