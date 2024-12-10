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


def find_reachable_hilltops(topo_map: dict[Point, int], current_pt: Point) -> list[Point]:
    if topo_map[current_pt] == 9:
        return [current_pt]

    hilltops: list[Point] = []

    for direction in {Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)}:
        next_pt = current_pt + direction
        if next_pt not in topo_map:
            continue

        if topo_map[next_pt] == topo_map[current_pt] + 1:
            hilltops.extend(find_reachable_hilltops(topo_map, next_pt))

    return hilltops


def solve(file_io: TextIO, star: Star = Star.ALL) -> None:
    topo_map = {Point(x, y): int(height) for y, line in enumerate(file_io) for x, height in enumerate(line.strip())}

    tailheads = [pt for pt, height in topo_map.items() if height == 0]

    tailheads_hilltops = [find_reachable_hilltops(topo_map, pt) for pt in tailheads]

    if star in {star.ALL, star.ONE}:
        s1 = sum(len(set(hilltops)) for hilltops in tailheads_hilltops)
        print(f"Star 1: {s1}")

    if star in {star.ALL, star.TWO}:
        s2 = sum(len(hilltops) for hilltops in tailheads_hilltops)

        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
