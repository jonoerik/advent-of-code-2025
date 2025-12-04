#!/usr/bin/env python3

import itertools
from pathlib import Path

# True if a roll of paper is present at that location.
InputType = list[list[bool]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [[{"@": True, ".": False}[c] for c in line.strip()] for line in f.readlines()]


def neighbour_count(input_data: InputType, r: int, c: int) -> int:
    return sum(
        1 if input_data[cur_r][cur_c] else 0
        for cur_r in range(max(0, r-1), min(len(input_data), r+2))
        for cur_c in range(max(0, c-1), min(len(input_data[0]), c+2))
        if not (cur_r == r and cur_c == c)
        )


def part1(input_data: InputType) -> ResultType:
    return sum(
        1 if neighbour_count(input_data, r, c) < 4 else 0
        for r, row in enumerate(input_data)
        for c, x in enumerate(row)
        if x
        )


def part2(input_data: InputType) -> ResultType:
    initial_count = sum(1 if x else 0 for row in input_data for x in row)
    any_changed = True
    while any_changed:
        any_changed = False
        for r, c in itertools.product(range(len(input_data)), range(len(input_data[0]))):
            if input_data[r][c] and neighbour_count(input_data, r, c) < 4:
                input_data[r][c] = False
                any_changed = True

    return initial_count - sum(1 if x else 0 for row in input_data for x in row)
