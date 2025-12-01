#!/usr/bin/env python3

from enum import Enum
from pathlib import Path

class Direction(Enum):
    L = 0
    R = 1

InputType = list[tuple[Direction, int]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [(
            {"L": Direction.L, "R": Direction.R}[line[0]],
            int(line[1:])
            ) for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    dial = 50
    result = 0
    for dir, dist in input_data:
        dial += dist * {Direction.L: -1, Direction.R: 1}[dir]
        dial %= 100
        if dial == 0:
            result += 1
    return result


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
