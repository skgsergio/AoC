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


def solve(file_io: TextIO, star: Star = Star.ALL) -> None:
    data = [int(n) for n in file_io.readline().strip()]

    if star in {star.ALL, star.ONE}:
        disk = data.copy()

        checksum = 0

        lbid = 0
        rbid = len(disk) // 2

        i = 0
        free_space = False
        while disk:
            size, disk = disk[0], disk[1:]

            if free_space:
                for _ in range(size):
                    checksum += i * rbid
                    i += 1

                    if disk[-1] == 1:
                        disk = disk[:-2]
                        rbid -= 1

                    else:
                        disk[-1] -= 1

            else:
                for _ in range(size):
                    checksum += i * lbid
                    i += 1

                lbid += 1

            free_space = not free_space

        s1 = checksum
        print(f"Star 1: {s1}")

    if star in {star.ALL, star.TWO}:
        disk = [[-1 if i % 2 else i // 2, size] for i, size in enumerate(data) if size > 0]

        src = 0
        while src < len(disk):
            src += 1

            fid, size = disk[-src]
            if fid == -1:
                continue

            for dst in range(len(disk) - src):
                if disk[dst][0] != -1 or disk[dst][1] < size:
                    continue

                # Same size -> replace in place
                if disk[dst][1] == size:
                    disk[dst][0] = fid

                # Different size -> substract size, insert before space
                else:
                    disk[dst][1] -= size
                    disk.insert(dst, disk[-src].copy())

                disk[-src][0] = -1
                break

        checksum = 0
        i = 0
        for fid, size in disk:
            checksum += int(fid * size * (i + ((size - 1) / 2))) if fid != -1 else 0
            i += size

        s2 = checksum
        print(f"Star 2: {s2}")


if __name__ == "__main__":
    main()
