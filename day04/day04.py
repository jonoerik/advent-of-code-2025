#!/usr/bin/env python3

from pathlib import Path

# True if a roll of paper is present at that location.
InputType = list[list[bool]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [[{"@": True, ".": False}[c] for c in line.strip()] for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    width = len(input_data[0])
    height = len(input_data)
    def neighbour_count(r: int, c: int) -> int:
        return sum(
            1 if input_data[cur_r][cur_c] else 0
            for cur_r in range(max(0, r-1), min(height, r+2))
            for cur_c in range(max(0, c-1), min(width, c+2))
            if not (cur_r == r and cur_c == c)
            )

    return sum(
        1 if neighbour_count(r, c) < 4 else 0
        for r, row in enumerate(input_data)
        for c, x in enumerate(row)
        if x
        )


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
