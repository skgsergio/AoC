#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
from enum import Enum
from typing import NamedTuple, TextIO


class Star(Enum):
    ALL = 0
    ONE = 1
    TWO = 2

    @staticmethod
    def argparse(value: str | int) -> Star:
        with contextlib.suppress(ValueError):
            value = int(value)

        if isinstance(value, int):
            return Star(value)

        if isinstance(value, str):
            try:
                return Star[value.lower().removeprefix("star.").upper()]
            except KeyError as e:
                raise ValueError from e

        return ValueError


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=argparse.FileType("r"), default="input")
    parser.add_argument("-s", "--star", type=Star.argparse, default=Star.ALL, choices=Star)

    args = parser.parse_args()

    solve(args.input, args.star)


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: object) -> Point:
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: object) -> Point:
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return Point(self.x - other.x, self.y - other.y)


class Element(Enum):
    EMPTY = "."
    OBSTACLE = "#"
    GUARD = "^"


DIRS = [
    Point(0, -1),  # ^
    Point(1, 0),   # >
    Point(0, 1),   # v
    Point(-1, 0),  # <
]


def obstacle_creates_loop(lab: dict[Point, Element], obstacle: Point, nxt_dir: int) -> bool:
    lab[obstacle] = Element.OBSTACLE

    visited: set[tuple[Point, int]] = set()

    current = obstacle - DIRS[nxt_dir]

    while current in lab:
        if (current, nxt_dir) in visited:
            lab[obstacle] = Element.EMPTY
            return True

        visited.add((current, nxt_dir))

        new = current + DIRS[nxt_dir]
        if new not in lab:
            break

        while lab[new] == Element.OBSTACLE:
            nxt_dir = (nxt_dir + 1) % len(DIRS)
            new = current + DIRS[nxt_dir]

        current = new

    lab[obstacle] = Element.EMPTY
    return False


def solve(file_io: TextIO, star: Star = Star.ALL) -> None:
    lab: dict[Point, Element] = {}
    guard = Point(-1, -1)

    for y, line in enumerate(file_io):
        for x, element in enumerate(line.strip()):
            pt = Point(x, y)
            lab[pt] = Element(element)

            if lab[pt] == Element.GUARD:
                lab[pt] = Element.EMPTY
                guard = pt

    visited: set[Point] = set()
    obstacle_loops: set[Point] = set()

    nxt_dir = 0
    current = guard

    while current in lab:
        visited.add(current)

        new = current + DIRS[nxt_dir]
        if new not in lab:
            break

        # If new possition is an obstacle make next possible 90º turn
        while lab[new] == Element.OBSTACLE:
            nxt_dir = (nxt_dir + 1) % len(DIRS)
            new = current + DIRS[nxt_dir]

        if star in {star.ALL, star.TWO} and \
           new not in visited and \
           obstacle_creates_loop(lab, new, nxt_dir):
            obstacle_loops.add(new)

        current = new

    if star in {star.ALL, star.ONE}:
        s1 = len(visited)
        print(f"Star 1: {s1}")

    if star in {star.ALL, star.TWO}:
        s2 = len(obstacle_loops)
        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
