#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
from enum import Enum
from typing import TYPE_CHECKING, NamedTuple, TextIO

if TYPE_CHECKING:
    from collections.abc import Iterator


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


class LetterSoup:
    def __init__(self) -> None:
        self.__grid: dict[Point, str] = {}

    def __getitem__(self, pt: Point) -> str:
        return self.__grid.get(pt, " ")

    def __setitem__(self, pt: Point, value: str) -> None:
        self.__grid[pt] = value

    def __iter__(self) -> Iterator[Point]:
        return iter(self.__grid)

    def word(self, pts: list[Point]) -> str:
        return "".join(self[pt] for pt in pts)

    def words(self, pt: Point, length: int = 4) -> list[str]:
        return [self.word(word_pts) for word_pts in [
            [pt + Point(i, 0) for i in range(length)],
            [pt + Point(0, i) for i in range(length)],
            [pt + Point(i, i) for i in range(length)],
            [pt + Point(-i, i) for i in range(length)],
        ]]

    class EvenValueError(Exception):
        def __init__(self) -> None:
            super().__init__("Length must be odd")

    def cross(self, pt: Point, length: int = 3) -> list[str]:
        if length % 2 != 1:
            raise self.EvenValueError

        half = length // 2

        return [self.word(word_pts) for word_pts in [
            [pt + Point(i, i) for i in range(-half, half + 1)],
            [pt + Point(-i, i) for i in range(-half, half + 1)],
        ]]


def solve(file_io: TextIO, star: Star = Star.ALL) -> None:
    soup = LetterSoup()

    for y, line in enumerate(file_io):
        for x, letter in enumerate(line):
            soup[Point(x, y)] = letter

    if star in {star.ALL, star.ONE}:
        s1 = sum(word in {"XMAS", "SAMX"} for pt in soup for word in soup.words(pt))

        print(f"Star 1: {s1}")

    if star in {star.ALL, star.TWO}:
        s2 = sum(all(word in {"MAS", "SAM"} for word in soup.cross(pt)) for pt in soup)

        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
