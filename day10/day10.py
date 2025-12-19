#!/usr/bin/env python3

import collections.abc
import heapq
import itertools
import numbers
from pathlib import Path
import re
import typing


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
    def a_star_admissible(f):
        """Mark heuristic function f as admissible as an A* heuristic."""
        f.is_a_star_admissible = True
        return f

    def a_star_consistent(f):
        """Mark heuristic function f as a consistent A* heuristic."""
        f.is_a_star_consistent = True
        return f

    def a_star_solve[
            T, C: numbers.Real
            ](
            start: T, goal: T,
            get_next_nodes: typing.Callable[[T], typing.Iterable[tuple[T, C]]],
            heuristic: typing.Callable[[T], C],
            ) -> C:
        """
        Solve a search problem using the A* algorithm, finding the cost to reach the goal.

        :param T: Type of nodes in the search graph.
        :param C: Type of edge cost. Probably int or float.
        :param start: Start node.
        :param goal: Target end node.
        :param get_next_nodes: Function taking a node, and returning an iterable that gives (next-node, cost) pairs.
        :param heuristic: Function taking a node, and returning the heuristic estimate of the cost from that node to the goal.
        :return: Best cost from start to goal.
        """
        assert getattr(heuristic, "is_a_star_admissible", False), "A* requries an admissible heuristic."

        # Set of nodes yet to be searched, as:
        # * Estimated total cost to goal (cost to reach + estimated cost to goal)
        # * Cost to reach this node from start
        # * Node
        open_set: list[tuple[C, C, T]] = [(heuristic(start), 0, start)]

        if getattr(heuristic, "is_a_star_consistent", False):
            visited: set[T] = {start}

            while open_set:
                _, current_cost, current_node = heapq.heappop(open_set)
                if current_node == goal:
                    return current_cost

                for next_node, next_cost in get_next_nodes(current_node):
                    tentative_cost = current_cost + next_cost
                    if next_node not in visited:
                        heapq.heappush(open_set, (tentative_cost + heuristic(next_node), tentative_cost, next_node))
                        visited.add(next_node)
        else:
            # Dictionary of node already visited, to the cost to reach that node from start.
            visited: dict[T, C] = {start: 0}

            while open_set:
                _, current_cost, current_node = heapq.heappop(open_set)
                if current_node == goal:
                    return current_cost

                for next_node, next_cost in get_next_nodes(current_node):
                    tentative_cost = current_cost + next_cost
                    if next_node not in visited or tentative_cost < visited[next_node]:
                        heapq.heappush(open_set, (tentative_cost + heuristic(next_node), tentative_cost, next_node))
                        visited[next_node] = tentative_cost

        raise RuntimeError("No path from start node to goal found")


    def min_button_presses(machine: Machine) -> int:
        def get_next_nodes(n: tuple[int, ...]) -> collections.abc.Generator[tuple[tuple[int, ...], int]]:
            for button in machine.buttons:
                next_node = tuple(x + 1 if i in button else x for i, x in enumerate(n))
                if all(next_val <= goal_val for next_val, goal_val in zip(next_node, machine.joltages, strict=True)):
                    yield next_node, 1

        @a_star_admissible
        @a_star_consistent
        def heuristic(n: tuple[int, ...]) -> int:
            #TODO explain heuristic, and why it's admissible and consistent.
            assert all(x <= g for x, g in zip(n, machine.joltages, strict=True))
            return max(g - x for x, g in zip(n, machine.joltages, strict=True))

        return a_star_solve((0,) * len(machine.joltages), machine.joltages, get_next_nodes, heuristic)

    return sum(min_button_presses(m) for m in input_data)
