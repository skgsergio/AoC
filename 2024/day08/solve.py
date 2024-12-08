#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
from collections import defaultdict
from enum import Enum
from itertools import combinations
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

    def in_range(self, lower: Point, upper: Point) -> bool:
        return lower.x <= self.x <= upper.x and lower.y <= self.y <= upper.y

    def __add__(self, other: object) -> Point:
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: object) -> Point:
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Point:
        return Point(-self.x, -self.y)


def solve(file_io: TextIO, star: Star = Star.ALL) -> None:  # noqa: C901
    frequencies: dict[str, list[Point]] = defaultdict(list)

    for y, line in enumerate(file_io):
        for x, element in enumerate(line.strip()):
            if element != ".":
                frequencies[element].append(Point(x, y))

    start = Point(0, 0)
    end = Point(x, y)

    antinodes: set[Point] = set()
    harmonics: set[Point] = set()

    for antennas in frequencies.values():
        for ant1, ant2 in combinations(antennas, 2):
            dist = ant2 - ant1

            if star in {star.ALL, star.ONE}:
                antinodes.update(pt for pt in {ant1 - dist, ant2 + dist} if pt.in_range(start, end))

            if star in {star.ALL, star.TWO}:
                for antinode, direction in {(ant1, -dist), (ant2, dist)}:
                    pt = antinode
                    while pt.in_range(start, end):
                        harmonics.add(pt)
                        pt += direction

    if star in {star.ALL, star.ONE}:
        s1 = len(antinodes)

        print(f"Star 1: {s1}")

    if star in {star.ALL, star.TWO}:
        s2 = len(harmonics)

        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
