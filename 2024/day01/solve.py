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


def solve(file_io: TextIO, star: Star = Star.ALL) -> None:
    left_list: list[int] = []
    right_list: list[int] = []

    for line in file_io:
        left, right = (int(n) for n in line.split())
        left_list.append(left)
        right_list.append(right)

    left_list.sort()
    right_list.sort()

    if star in [star.ALL, star.ONE]:
        s1 = sum(abs(left - right) for left, right in zip(left_list, right_list, strict=True))

        print(f"Star 1: {s1}")

    if star in [star.ALL, star.TWO]:
        # Assuming left values do not repeat a lot so not caching count() result in a dict
        s2 = sum(left * right_list.count(left) for left in left_list)

        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
