#!/usr/bin/env python3

from enum import Enum
import itertools
import math
from pathlib import Path
import typing

InputType = list[tuple[int, int]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path, encoding="utf-8") as f:
        result = [tuple(int(x) for x in line.strip().split(",")) for line in f.readlines()]
    assert all(len(coord) == 2 for coord in result)
    return result


def part1(input_data: InputType) -> ResultType:
    return max(math.prod(abs(x - y + 1)
                         for x, y in zip(a, b, strict=True))
               for a, b in itertools.combinations(input_data, 2))


def part2(input_data: InputType) -> ResultType:
    type Point = tuple[int, int]

    class Rect:
        def __init__(self, xs: range, ys: range):
            self.xs = xs
            self.ys = ys

        def intersection(self, other: "Rect") -> typing.Optional["Rect"]:
            left = max(self.xs.start, other.xs.start)
            right = min(self.xs.stop, other.xs.stop)
            top = max(self.ys.start, other.ys.start)
            bottom = min(self.ys.stop, other.ys.stop)

            if left < right and top < bottom:
                return Rect(range(left, right), range(top, bottom))
            else:
                return None

        def contains(self, other: "Rect") -> bool:
            return (self.xs.start <= other.xs.start and
                    self.xs.stop >= other.xs.stop and
                    self.ys.start <= other.ys.start and
                    self.ys.stop >= other.ys.stop)

        def __str__(self) -> str:
            return f"({self.xs.start},{self.ys.start}) - ({self.xs.stop - 1},{self.ys.stop - 1})"

    class BSPNodeState(Enum):
        ALL_FALSE = 0
        ALL_TRUE = 1
        SPLIT = 2
    bsp_node_state_to_bool = {
        BSPNodeState.ALL_FALSE: False,
        BSPNodeState.ALL_TRUE: True,
    }

    class BSPNode:
        def __init__(self, bounds: Rect, value: bool):
            self.children: list[BSPNode] = []
            self.state: BSPNodeState = BSPNodeState.ALL_TRUE if value else BSPNodeState.ALL_FALSE
            # X and Y bounds for this node. As with ranges, this includes the start coordinates
            # but excludes the end coordinates.
            self.bounds: Rect = bounds

        def set_rect(self, r: Rect, value: bool) -> None:
            if r.contains(self.bounds):
                self.state = BSPNodeState.ALL_TRUE if value else BSPNodeState.ALL_FALSE
                self.children = []

            elif cross := self.bounds.intersection(r):
                if self.state != BSPNodeState.SPLIT:
                    if cross.xs.start != self.bounds.xs.start:
                        self.split_vertical(cross.xs.start)
                    elif cross.xs.stop != self.bounds.xs.stop:
                        self.split_vertical(cross.xs.stop)
                    elif cross.ys.start != self.bounds.ys.start:
                        self.split_horizontal(cross.ys.start)
                    elif cross.ys.stop != self.bounds.ys.stop:
                        self.split_horizontal(cross.ys.stop)

                assert self.state == BSPNodeState.SPLIT
                for child in self.children:
                    child.set_rect(r, value)

            else:
                pass

        def split_vertical(self, x: int):
            assert self.state != BSPNodeState.SPLIT
            assert self.bounds.xs.start < x < self.bounds.xs.stop
            self.children = {
                BSPNode(Rect(range(self.bounds.xs.start, x), self.bounds.ys), bsp_node_state_to_bool[self.state]),
                BSPNode(Rect(range(x, self.bounds.xs.stop), self.bounds.ys), bsp_node_state_to_bool[self.state])
            }
            self.state = BSPNodeState.SPLIT

        def split_horizontal(self, y: int):
            assert self.state != BSPNodeState.SPLIT
            assert self.bounds.ys.start < y < self.bounds.ys.stop
            self.children = {
                BSPNode(Rect(self.bounds.xs, range(self.bounds.ys.start, y)), bsp_node_state_to_bool[self.state]),
                BSPNode(Rect(self.bounds.xs, range(y, self.bounds.ys.stop)), bsp_node_state_to_bool[self.state])
            }
            self.state = BSPNodeState.SPLIT

        def traverse_leaves(self, f: typing.Callable[["BSPNode"], typing.Any]) -> list[typing.Any]:
            if self.state == BSPNodeState.SPLIT:
                return [result for child in self.children for result in child.traverse_leaves(f)]
            else:
                return [f(self)]

        def point_state(self, p: Point) -> bool:
            assert p[0] in self.bounds.xs and p[1] in self.bounds.ys
            match self.state:
                case BSPNodeState.ALL_FALSE:
                    return False
                case BSPNodeState.ALL_TRUE:
                    return True
                case BSPNodeState.SPLIT:
                    results = [child.point_state(p) for child in self.children
                               if p[0] in child.bounds.xs and p[1] in child.bounds.ys]
                    # Child regions should be non-overlapping.
                    assert len(results) == 1
                    return results[0]

        def __str__(self) -> str:
            return (str(self.bounds) + "\n" +
                    "\n".join(
                        "".join(
                            "#" if self.point_state((x, y)) else "."
                            for x in self.bounds.xs)
                        for y in self.bounds.ys
                    )
                )

    class Poly:
        def __init__(self, points: list[Point]):
            left = min(x for x, _ in points)
            right = max(x for x, _ in points)
            top = min(y for _, y in points)
            bottom = max(y for _, y in points)
            self.bsp = BSPNode(Rect(range(left, right + 1), range(top, bottom + 1)), False)

            for a, b in itertools.pairwise(points + [points[0]]):
                self.bsp.set_rect(Rect(range(min(a[0], b[0]), max(a[0], b[0]) + 1),
                                       range(min(a[1], b[1]), max(a[1], b[1]) + 1)),
                                  True)

            def colour_internal_regions(node: BSPNode) -> None:
                if node.state == BSPNodeState.ALL_FALSE:
                    # If this region is ALL_FALSE, it doesn't lie on an edge line,
                    # so we need to check if it lies inside the polygon.
                    # First, select an arbitrary point (here, the upper-left corner of the region).
                    x, y = node.bounds.xs.start, node.bounds.ys.start
                    # So that we don't have to think about handling vertical edges directly above the point,
                    # we adjust our comparisons so that we're effectively testing (x + 0.5, y + 0.5).

                    # Find the number of times a line from that point to the top edge crosses an edge.
                    edge_crossings = sum(1 if (
                        a[1] == b[1] and  # Edge is horizontal.
                        min(a[0], b[0]) <= x < max(a[0], b[0]) and  # Edge extends left/right to cover the point.
                        y >= a[1]  # Edge is above the point.
                    ) else 0 for a, b in itertools.pairwise(points + [points[0]]))

                    if edge_crossings % 2 == 1:
                        node.state = BSPNodeState.ALL_TRUE

            self.bsp.traverse_leaves(colour_internal_regions)

        def covers(self, r: Rect) -> bool:
            """Return true if the polygon completely covers the rectangle between corners a and b."""
            # Top BSP node should completely cover the queried area.
            assert self.bsp.bounds.contains(r)

            def covered_area_true(node: BSPNode) -> bool:
                match r.intersection(node.bounds):
                    case Rect():
                        return bsp_node_state_to_bool[node.state]
                    case None:
                        return True

            return all(self.bsp.traverse_leaves(covered_area_true))

    poly = Poly(input_data)
    test_rects = sorted(
            (Rect(range(min(a[0], b[0]), max(a[0], b[0]) + 1),
                  range(min(a[1], b[1]), max(a[1], b[1]) + 1))
                for a, b in itertools.combinations(input_data, 2)),
            key=lambda r: len(r.xs) * len(r.ys),
            reverse=True
        )
    return next(
            len(r.xs) * len(r.ys)
            for r in test_rects
            if poly.covers(r)
        )
