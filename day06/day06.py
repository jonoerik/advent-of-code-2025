#!/usr/bin/env python3

from enum import Enum
import math
from pathlib import Path

InputType = list[str]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        # Just remove trailling newline.
        return [line.removesuffix("\n") for line in f.readlines()]


class Op(Enum):
    ADD = 0
    MULTIPLY = 1


def part1(input_data: InputType) -> ResultType:
    numbers = [[int(s) for s in line.strip().split()] for line in input_data[:-1]]
    ops = [{"+": Op.ADD, "*": Op.MULTIPLY}[s] for s in input_data[-1].strip().split()]
    return sum([
        ({Op.ADD: sum, Op.MULTIPLY: math.prod}[op])([line[i] for line in numbers])
        for i, op in enumerate(ops)
        ])


def part2(input_data: InputType) -> ResultType:
    # Take the input as a grid of characters, and rotate it 90 degrees counter-clockwise.
    line_length = len(input_data[0])
    assert all(len(line) == line_length for line in input_data)
    input_data = ["".join([line[i] for line in input_data]).strip() for i in range(-1, -line_length - 1, -1)]
    # Remove blank lines.
    input_data = [line for line in input_data if len(line) > 0]

    # input_data will now be a list of strings representing numbers to be added/multiplied.
    # The final number in each problem will end with either + or *, indicating the operation to be performed on
    # the preceeding numbers.

    result = 0
    previous_numbers = []
    for line in input_data:
        if line.endswith("+"):
            previous_numbers.append(int(line[:-1]))
            result += sum(previous_numbers)
            previous_numbers = []
        elif line.endswith("*"):
            previous_numbers.append(int(line[:-1]))
            result += math.prod(previous_numbers)
            previous_numbers = []
        else:
            previous_numbers.append(int(line))

    assert not previous_numbers
    return result
