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
    # length of number -> sub-string lengths that we need to check for repetitions.
    repetition_lengths: dict[int, list[int]] = {
        l: []
        for l in range(2, max([math.floor(math.log10(i)) + 1 for _, i in input_data]) + 1)
    }
    for k in repetition_lengths.keys():
        for i in range(math.ceil(k / 2), 0, -1):
            if k % i == 0 and not any([j % i == 0 for j in repetition_lengths[k]]):
                repetition_lengths[k].append(i)
    # e.g. for a number of length 12, we need to check for repetitions of length 3 or 4 (factors of 12).
    # We don't need to check for repetitions of length 3, 2, or 1, as these will be detected as repetitions of 3 or 4.

    def generate_factor(num_length: int, repetition_length: int) -> int:
        result = 0
        for i in range(num_length // repetition_length):
            result *= 10 ** repetition_length
            result += 1
        return result
    # length of number -> potential factors of the number, which indicate a sequence of repeated digits.
    factors: dict[int, list[int]] = {
        k: [generate_factor(k, v) for v in vs]
        for k, vs in repetition_lengths.items()
    }

    # A single digit number can never be a repeated pattern.
    factors[1] = []

    def repeated_numbers(start: int, end: int) -> list[int]:
        result = []

        for i in range(start, end + 1):
            i_length = math.floor(math.log10(i)) + 1
            if any([i % f == 0 for f in factors[i_length]]):
                result.append(i)

        return result
    return sum([sum(repeated_numbers(start, end)) for start, end in input_data])
