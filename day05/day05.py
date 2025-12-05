#!/usr/bin/env python3

from pathlib import Path

InputType = tuple[list[tuple[int, int]], list[int]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        ranges = []
        while line := f.readline().strip():
            ranges.append(tuple(int(x) for x in line.split("-", 2)))
        ingredients = [int(x.strip()) for x in f.readlines()]
    return ranges, ingredients


def part1(input_data: InputType) -> ResultType:
    ranges = set(range(a, b + 1) for a, b in input_data[0])
    return sum(1 if any(ingredient in r for r in ranges) else 0 for ingredient in input_data[1])


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
