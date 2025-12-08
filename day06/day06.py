#!/usr/bin/env python3

from enum import Enum
import math
from pathlib import Path

class Op(Enum):
    ADD = 0
    MULTIPLY = 1

InputType = tuple[list[list[int]], list[Op]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        lines: list[list[str]] = [line.strip().split() for line in f.readlines()]
        return ([[int(s) for s in line] for line in lines[:-1]],
                [{"+": Op.ADD, "*": Op.MULTIPLY}[s] for s in lines[-1]])


def part1(input_data: InputType) -> ResultType:
    return sum([
        ({Op.ADD: sum, Op.MULTIPLY: math.prod}[op])([line[i] for line in input_data[0]])
        for i, op in enumerate(input_data[1])
        ])


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
