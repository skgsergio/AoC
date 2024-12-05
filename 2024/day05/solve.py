#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
from enum import Enum
from functools import cmp_to_key
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


def middle(prod: list[int] | tuple[int, ...]) -> int:
    return prod[(len(prod) - 1) // 2]


def solve(file_io: TextIO, star: Star = Star.ALL) -> None:
    part1, part2 = file_io.read().split("\n\n")

    rules = {tuple(int(n) for n in rule.split("|")) for rule in part1.split()}
    prods = {tuple(int(n) for n in prod.split(",")) for prod in part2.split()}

    valid_prods = set()
    for prod in prods:
        if all(prod.index(p1) < prod.index(p2) for p1, p2 in rules if p1 in prod and p2 in prod):
            valid_prods.add(prod)

    if star in {star.ALL, star.ONE}:
        s1 = sum(middle(prod) for prod in valid_prods)

        print(f"Star 1: {s1}")

    if star in {star.ALL, star.TWO}:
        s2 = sum(
            middle(sorted(prod, key=cmp_to_key(lambda p1, p2: -1 if (p1, p2) in rules else 1)))
            for prod in prods - valid_prods
        )

        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
