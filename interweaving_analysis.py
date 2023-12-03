"""
This script is used to generate the data for the runtime analysis of the
algorithm for determining if s is an interweaving of x and y. Given a file
that has strings of 0's and 1's on each line, this script checks if that string
is an interweaving of 101 and 010.
"""

import sys

from interweaving import Interweaving

X = "101"
Y = "010"


def interweaving_analysis(data: list[str], i: int, s: str):
    weaving = Interweaving(s, X, Y)
    is_interweaving = weaving.is_interweaving()
    data.append(f"{i},{len(s)},{weaving.counter},{is_interweaving}")


def main(argv: list[str]):
    if len(argv) < 2:
        print("Not enough arguments provided.")
        return

    data = []
    with open(argv[1], "r") as f:
        for i, s in enumerate(f.readlines()):
            interweaving_analysis(data, i, s.strip())
    print("\n".join(data))


if __name__ == "__main__":
    main(sys.argv)
