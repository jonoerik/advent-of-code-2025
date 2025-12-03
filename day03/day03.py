#!/usr/bin/env python3

from pathlib import Path

InputType = list[list[int]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [[int(x) for x in line.strip()] for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    return sum([
        max([
            bank[i] * 10 + bank[j]
            for i in range(len(bank))
            for j in range(len(bank))
            if i < j
        ])
        for bank in input_data
    ])


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
