#!/usr/bin/env python3

import functools
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
    def ranges_intersect(a: tuple[int, int], b: tuple[int, int]) -> bool:
        return (a[0] <= b[0] <= a[1]) or (a[0] <= b[1] <= a[1]) or (b[0] <= a[0] and b[1] >= a[1])

    def merge_ranges(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
        assert ranges_intersect(a, b)
        return min(a[0], b[0]), max(a[1], b[1])

    ranges = []
    for new_range in input_data[0]:
        to_merge = [r for r in ranges if ranges_intersect(r, new_range)]
        ranges = [r for r in ranges if r not in to_merge]
        ranges.append(functools.reduce(merge_ranges, to_merge, new_range))

    return sum([b - a + 1 for a, b in ranges])
