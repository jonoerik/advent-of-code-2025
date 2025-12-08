#!/usr/bin/env python3

from enum import Enum
import math
from pathlib import Path

class Op(Enum):
    ADD = 0
    MULTIPLY = 1

InputType = list[str]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return f.readlines()



def part1(input_data: InputType) -> ResultType:
    numbers = [[int(s) for s in line.strip().split()] for line in input_data[:-1]]
    ops = [{"+": Op.ADD, "*": Op.MULTIPLY}[s] for s in input_data[-1].strip().split()]
    return sum([
        ({Op.ADD: sum, Op.MULTIPLY: math.prod}[op])([line[i] for line in numbers])
        for i, op in enumerate(ops)
        ])


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
