#!/usr/bin/env python3

from enum import Enum
from pathlib import Path

class Tile(Enum):
    START = 0
    EMPTY = 1
    SPLITTER = 2

InputType = list[list[Tile]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [[{"S": Tile.START, ".": Tile.EMPTY, "^": Tile.SPLITTER}[c]
                 for c in line.strip()]
                for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    beams = set(i for i, t in enumerate(input_data[0]) if t == Tile.START)
    num_splits = 0
    for row in input_data[1:]:
        num_splits += sum(1 for i, t in enumerate(row) if t == Tile.SPLITTER and i in beams)
        beams = (
            set(beam for beam in beams if row[beam] == Tile.EMPTY)
            | set(split_beam
                  for beam in beams if row[beam] == Tile.SPLITTER
                  for split_beam in (beam - 1, beam + 1) if 0 <= split_beam < len(row))
            )
    return num_splits


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
