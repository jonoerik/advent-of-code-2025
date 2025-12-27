#!/usr/bin/env python3

import itertools
from pathlib import Path
import pulp
import re


class Machine:
    LightsType = tuple[bool, ...]
    ButtonsType = tuple[tuple[int, ...], ...]
    JoltagesType = tuple[int, ...]

    def __init__(self, lights: LightsType, buttons: ButtonsType, joltages: JoltagesType):
        self.lights = lights
        self.buttons = buttons
        self.joltages = joltages

    def __str__(self) -> str:
        return (f"[{"".join({False: ".", True: "#"}[x] for x in self.lights)}] "
                f"{" ".join(f"({",".join([str(b) for b in button])})" for button in self.buttons)} "
                f"{{{",".join(str(j) for j in self.joltages)}}}")


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
        lights = tuple({".": False, "#": True}[c] for c in match.group("lights"))
        buttons = tuple([int(x) for x in button.lstrip("(").rstrip(")").split(",")] for button in match.group("buttons").split())
        joltages = tuple(int(x) for x in match.group("joltages").split(","))
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
            lights = (False,) * len(machine.lights)

            for button in (machine.buttons[i] for i, b in enumerate(button_presses) if b):
                lights = tuple(x ^ True if i in button else x for i, x in enumerate(lights))

            if lights == machine.lights:
                return button_presses.count(True)

    return sum(min_button_presses(m) for m in input_data)


def part2(input_data: InputType) -> ResultType:
    def min_button_presses(machine: Machine) -> int:
        # This is an integer programming problem.
        # Variables are the number of times each button is pressed.
        # Goal is to minimise sum of button variables.
        # We have 1 constraint per joltage.

        problem = pulp.LpProblem(sense=pulp.LpMinimize)
        button_vars = [pulp.LpVariable(name=f"button_{i}", lowBound=0, cat="Integer")
                       for i in range(len(machine.buttons))]
        problem += sum(button_vars)
        for i, j in enumerate(machine.joltages):
            problem += sum(bv for bv, b in zip(button_vars, machine.buttons, strict=True) if i in b) == j
        problem.solve(pulp.PULP_CBC_CMD(msg=False))
        assert pulp.LpStatus[problem.status] == "Optimal"
        return int(sum(v.varValue for v in problem.variables()))

    return sum(min_button_presses(m) for m in input_data)
