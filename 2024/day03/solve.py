#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import re
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
    memory = "\n".join(file_io.readlines())

    ops = re.finditer(
        r"(?P<OP>mul|do(?:n't)?)\((?:(?P<N1>\d+),(?P<N2>\d+))?\)",
        memory,
        re.MULTILINE,
    )

    s1 = 0
    s2 = 0
    enabled = True

    for op in ops:
        match op.groups():
            case ("mul", n1, n2):
                value = int(n1) * int(n2)

                s1 += value

                if enabled:
                    s2 += value

            case ("do", None, None):
                enabled = True

            case ("don't", None, None):
                enabled = False

    if star in {star.ALL, star.ONE}:
        print(f"Star 1: {s1}")

    if star in {star.ALL, star.TWO}:
        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
