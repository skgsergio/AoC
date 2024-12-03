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

        raise ValueError


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=argparse.FileType("r"), default="input")
    parser.add_argument("-s", "--star", type=Star.argparse, default=Star.ALL, choices=Star)

    args = parser.parse_args()

    solve(args.input, args.star)


def safe(report: list[int]) -> bool:
    sorted_report = sorted(report)

    if report != sorted_report and report != sorted_report[::-1]:
        return False

    return all(1 <= abs(report[i - 1] - report[i]) <= 3 for i in range(1, len(report)))


def safe_with_dampen(report: list[int]) -> bool:
    if safe(report):
        return True

    return any(safe(report[:i] + report[i + 1 :]) for i in range(len(report)))


def solve(file_io: TextIO, star: Star = Star.ALL) -> None:
    reports: list[list[int]] = [[int(n) for n in line.split()] for line in file_io]

    if star in {star.ALL, star.ONE}:
        s1 = sum(safe(report) for report in reports)

        print(f"Star 1: {s1}")

    if star in {star.ALL, star.TWO}:
        s2 = sum(safe_with_dampen(report) for report in reports)

        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
