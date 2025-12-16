#!/usr/bin/env python3

import itertools
from pathlib import Path
import re


class Machine:
    LightsType = list[bool]
    ButtonsType = list[list[int]]
    JoltagesType = list[int]

    def __init__(self, lights: LightsType, buttons: ButtonsType, joltages: JoltagesType):
        self.lights = lights
        self.buttons = buttons
        self.joltages = joltages

    def __str__(self) -> str:
        return (f"[{"".join([{False: ".", True: "#"}[x] for x in self.lights])}] "
                f"{" ".join([f"({",".join([str(b) for b in button])})" for button in self.buttons])} "
                f"{{{",".join([str(j) for j in self.joltages])}}}")


InputType = list[Machine]
ResultType = int


def load(input_path: Path) -> InputType:
    line_regex = re.compile(r"^"
                            r"\[(?P<lights>[.#]*)\]\s*"
                            r"(?P<buttons>\(\d+(?:,\d+)*\)?(?:\s+\(\d+(?:,\d+)*\)?)*)?\s*"
                            r"{(?P<joltages>\d+(?:,\d+)*)?}"
                            r"$")
    def parse_machine(line: str) -> Machine:
        match = line_regex.fullmatch(line)
        assert match
        lights = [{".": False, "#": True}[c] for c in match.group("lights")]
        buttons = [[int(x) for x in button.lstrip("(").rstrip(")").split(",")] for button in match.group("buttons").split()]
        joltages = [int(x) for x in match.group("joltages").split(",")]
        return Machine(lights, buttons, joltages)

    with open(input_path) as f:
        return [parse_machine(line.strip()) for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    def min_button_presses(machine: Machine) -> int:
        # Pressing a button twice has the same effect as not pressing it at all.
        # So the required lights state will be reached by pressing each button 0 or 1 times.
        # In the input data file, machines have at most 13 buttons, giving 2**13 possibilities to check,
        # which is small enough to search by brute force.

        for button_presses in sorted(itertools.product((False, True), repeat=len(machine.buttons)), key=lambda x: x.count(True)):
            lights = [False] * len(machine.lights)

            for button_index in (i for i, b in enumerate(button_presses) if b):
                for light_index in machine.buttons[button_index]:
                    lights[light_index] ^= True

            if lights == machine.lights:
                return button_presses.count(True)

    return sum(min_button_presses(m) for m in input_data)


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
