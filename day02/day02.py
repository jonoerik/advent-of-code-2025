#!/usr/bin/env python3

import math
from pathlib import Path

InputType = list[tuple[int, int]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        result = [tuple([int(y) for y in x.split("-")]) for x in f.read().strip().split(",")]
    assert all([len(x) == 2 for x in result])
    return result


def part1(input_data: InputType) -> ResultType:
    def repeated_numbers(start: int, end: int) -> list[int]:
        result = []

        for i in range(start, end + 1):
            i_length = math.floor(math.log10(i)) + 1
            if i_length % 2 == 1:
                continue
            # e.g. A 6 digit number will have 1001 as a factor iff it is a twice-repeated sequence of 3 digits.
            if i % (10 ** (i_length // 2) + 1) == 0:
                result.append(i)

        return result
    return sum([sum(repeated_numbers(start, end)) for start, end in input_data])


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
