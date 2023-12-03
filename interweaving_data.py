import sys
import random

characters = ["0", "1"]


def main(argv: list[str]):
    if len(argv) <= 2:
        print("Not enough arguments.")
        return -1

    try:
        number_of_strings = int(argv[1])
        if number_of_strings <= 0:
            print("The prvided first argument was not a positive integer!")
            raise Exception
        string_length = int(argv[2])
    except Exception:
        return -1

    strings = []
    for _ in range(number_of_strings):
        string = []
        for _ in range(string_length):
            i = int(random.random() * 2)  # 0 or 1 with equal probability
            string.append(characters[i])
        strings.append("".join(string))
    for string in strings:
        print(string)


if __name__ == "__main__":
    main(sys.argv)
