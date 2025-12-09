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
    beams = [1 if input_data[0][i] == Tile.START else 0 for i in range(len(input_data[0]))]

    for row in input_data[1:]:
        beams = [(beams[i] if tile == Tile.EMPTY else 0) +
                 (beams[i-1] if i > 0 and row[i-1] == Tile.SPLITTER else 0) +
                 (beams[i+1] if i < len(row) - 1 and row[i+1] == Tile.SPLITTER else 0)
                 for i, tile in enumerate(row)]

    return sum(beams)
