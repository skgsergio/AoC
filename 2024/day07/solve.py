#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
from enum import Enum
from typing import TextIO


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


def is_possible(value: int, current: int, rest: list[int], *, concatenation: bool = False) -> bool:
    if not rest:
        return value == current

    if current > value:
        return False

    if is_possible(value, current + rest[0], rest[1:], concatenation=concatenation):
        return True

    if is_possible(value, current * rest[0], rest[1:], concatenation=concatenation):
        return True

    return concatenation and is_possible(value, int(f"{current}{rest[0]}"), rest[1:], concatenation=concatenation)


def solve(file_io: TextIO, star: Star = Star.ALL) -> None:
    equations: list[tuple[int, list[int]]] = []

    for line in file_io:
        value, nums = line.split(":")

        equations.append((int(value), [int(num) for num in nums.split()]))

    if star in {star.ALL, star.ONE}:
        s1 = sum(value for value, nums in equations if is_possible(value, nums[0], nums[1:]))

        print(f"Star 1: {s1}")

    if star in {star.ALL, star.TWO}:
        s2 = sum(value for value, nums in equations if is_possible(value, nums[0], nums[1:], concatenation=True))

        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
