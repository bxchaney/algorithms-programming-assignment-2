from typing import Tuple, Union

class Colors:

    grey = "\033[90m"
    blue = "\033[94m"
    red = "\033[91m"
    end = "\033[0m"



def clrs_lcs(s: str, x: str) -> Tuple[list[list[int]], list[list[str]]]:
    # number of possible repetitions
    reps = len(s) // len(x)

    # longest possible substring of complete repetitions
    substr_length = reps * len(x)

    c = [[0 for _ in range(substr_length + 1)] for _ in range(len(s) + 1)]
    b = [["" for _ in range(substr_length + 1)] for _ in range(len(s) + 1)]

    for i in range(1, len(s) + 1):
        for j in range(1, len(c[0])):
            if s[i - 1] == x[(j - 1) % len(x)]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = "\\"
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = "^"
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = "<"
    return c, b


def get_reps(b: list[list[str]], x: str, i: int, j: int) -> list[list[int]]:
    strings = []

    def get_lcs(b: list[list[str]], s: list[int], x: str, i: int, j: int):
        if i == 0 or j == 0:
            strings.append(s[::-1])
            return
        if b[i][j] == "\\":
            # if points to ^ and above is \\, then recurse
            if b[i - 1][j - 1] == "^" and (b[i - 1][j] in ["\\", "^"]) :
            #if b[i - 1][j - 1] == "^" and (b[i - 1][j] in ["\\"]) :
                new_s = s.copy()
                get_lcs(b, new_s, x, i - 1, j)
            s.append(i - 1)
            get_lcs(b, s, x, i - 1, j - 1)
        elif b[i][j] == "^":
            get_lcs(b, s, x, i - 1, j)

        else:
            get_lcs(b, s, x, i, j - 1)

    while i > 0:
        get_lcs(b, [], x, i, j)
        i -= 1

    return strings


def get_sets(str1, str2):
    c, b = clrs_lcs(str1, str2)
    for i in range(len(c)):
        print( ", ".join([f"{v}{ch}" for v, ch in zip(c[i], b[i])]))
            
    i = 0
    last_row = c[-1]
    while i < len(last_row) - 1:
        if last_row[i] + 1 == last_row[i + 1]:
            i += 1
        else:
            break
    return get_reps(b, str1, len(str1), i - (i % len(str2)))


def is_interleaving(s: str, x: str, y: str) -> Tuple[bool, Union[Tuple, None]]:
    reps_of_x = get_sets(s, x)
    reps_of_y = get_sets(s, y)
    print(reps_of_x)
    print(reps_of_y)

    minimum = len(s)
    maximum = 0
    for rep_x in reps_of_x:
        minimum = min(minimum, rep_x[0])
        maximum = max(maximum, rep_x[-1])
    for rep_y in reps_of_y:
        minimum = min(minimum, rep_y[0])
        maximum = max(maximum, rep_y[-1])

    for rep_x in reps_of_x:
        x_set = set(rep_x)
        for rep_y in reps_of_y:
            res = check_sets(s, x_set, x, set(rep_y), y, minimum, maximum)
            if res is not None:
                return True, res
    return False, None


def check_sets(
    s: str,
    x_set: set[int],
    x: str,
    y_set: set[int],
    y: str,
    minimum: int,
    maximum: int,
):
    union = x_set | y_set
    intersection = x_set & y_set
    for i in range(minimum, maximum + 1):
        # if the union is not a continuous string
        if i not in union:
            return None

    # if we can remove the intesection of x_set and y_set from either
    # x_set or from y_set, then we have an interleaving. That is, if
    # x_set - (x_set & y_set) is a non-empty repetition of x or if
    # y_set - (x_set & y_set) is a non-empty repetition of y then we have
    # a repetition
    if is_rep(s, x_set - intersection, x):
        return (x_set - intersection, y_set)
    if is_rep(s, y_set - intersection, y):
        return (x_set, y_set - intersection)

    return None


def is_rep(s: str, x_set: set[int], x: str) -> bool:
    if len(x) == 1 and len(x_set) != 0:
        return True
    if len(x_set) % len(x) != 0:
        return False
    x_list = [i for i in x_set]
    x_list.sort()
    for i, v in enumerate(x_list):
        if not x[i % len(x)] == s[v]:
            return False
    return True

def print_res(res: Tuple[bool, Tuple[set[int]]], s:str, x:str, y:str) -> None:
    print(f"s: {s}")
    print(f"x: {Colors.blue}{x}{Colors.end}")
    print(f"y: {Colors.red}{y}{Colors.end}")

    out = []
    x_set = res[1][0]
    y_set = res[1][1]
    for i, c in enumerate(s):
        if i in x_set:
            out.append(f"{Colors.blue}{c}{Colors.end}")
        elif i in y_set:
            out.append(f"{Colors.red}{c}{Colors.end}")
        else:
            out.append(f"{Colors.grey}{c}{Colors.end}")
    print("".join(out))



# Driver program to run the case
if __name__ == "__main__":
    
    s = "010101"
    x = "101"
    y = "010"
    res = is_interleaving(s, x, y)
    if res[0]:
        print_res(res, s, x, y)

    # prinlAllLCSSorted(str1, str2)
