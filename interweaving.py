from math import gcd
import sys
from typing import Tuple


class Interweaving:
    def __init__(self, s: str, x: str, y: str) -> None:
        self.counter = 0
        self._s = s
        self._x = x
        self._y = y
        self._dp = [[]]

    def _set_dp_table(self, s: str) -> None:
        len_x_k = len(self._x) * (len(s) // len(self._x))
        len_y_k = len(self._y) * (len(s) // len(self._y))
        self._dp = [
            [False for _ in range(len_y_k + 1)] for _ in range(len_x_k + 1)
        ]

    def check_substrings(
        self,
        s: str,
    ) -> None:
        self._set_dp_table(s)
        len_x_k = len(self._x) * (len(s) // len(self._x))
        len_y_k = len(self._y) * (len(s) // len(self._y))

        self.counter += 1
        for i in range(len_x_k + 1):
            self.counter += 1
            for j in range(len_y_k + 1):
                self.counter += 2
                if i + j > len(s):
                    continue

                self.counter += 1
                if i == 0 and j == 0:
                    self._dp[i][j] = True

                elif i == 0:
                    self.counter += 3
                    self._dp[i][j] = (
                        self._dp[i][j - 1]
                        and self._y[(j - 1) % len(self._y)] == s[i + j - 1]
                    )

                elif j == 0:
                    self.counter += 4
                    self._dp[i][j] = (
                        self._dp[i - 1][j]
                        and self._x[(i - 1) % len(self._x)] == s[i + j - 1]
                    )

                else:
                    self.counter += 6
                    self._dp[i][j] = (
                        self._dp[i - 1][j]
                        and self._x[(i - 1) % len(self._x)] == s[i + j - 1]
                    ) or (
                        self._dp[i][j - 1]
                        and self._y[(j - 1) % len(self._y)] == s[i + j - 1]
                    )

    def check_linear_combinations(self, s: str) -> bool:
        """
        After check_substrings stores it's results in _dp, we search dp to find
        determine if s is an interweaving of repetitions of x and y. We do not
        know ahead of time what the length x_k and y_k are, so we search _dp
        for the entires that correspond to x_k and y_k such that:

            len(x_k) + len(y_k) = len(s).

        Note that this equality may be restated as follows. If the length of
        the string x is a, the length of the string y is b, and the length of
        the string s is c, then we need values of m,n > 0 such that:

                             an + bm = c

        This is the Diophantine Equation, and there is a solution iff gcd(n,m)
        divides c.
        """
        self.check_substrings(s)
        candidates = self.get_candidate_solutions(
            len(self._x), len(self._y), len(s)
        )

        self.counter += 1
        for i, j in candidates:
            self.counter += 2
            if self._dp[len(self._x) * i][len(self._y) * j]:
                return True

        return False

    def is_interweaving(self) -> bool:
        self.counter += 1
        for c in self._s:
            self.counter += 1
            if c not in ["0", "1"]:
                return False
        match_found = False
        s_begin = 0
        for i, c in enumerate(self._s):
            self.counter += 1
            if self._s[i] in [self._x[0], self._y[0]]:
                s_begin = i
                match_found = True
                break
        if not match_found:
            return False

        s = self._s[s_begin:]

        s_end = len(s)
        self.counter += 1
        # Necessary condition to have complete repetitions of x and y
        while s_end % gcd(len(self._x), len(self._y)) != 0:
            self.counter += 1
            s_end -= 1

        if s_end < len(self._x) + len(self._y):
            return False

        s = s[:s_end]

        return self.check_linear_combinations(s)

    def modified_bezout(self, a: int, b: int, c: int) -> Tuple[int, int]:
        s = 0
        r = b
        old_s = 1
        old_r = a

        self.counter += 1
        while r != 0:
            self.counter += 1
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s

        self.counter += 1
        if b != 0:
            t = (old_r - old_s * a) // b
        else:
            t = 0

        # old_r has the gcd
        return (old_s * (c // old_r), t * (c // old_r))

    def get_candidate_solutions(
        self, a: int, b: int, c: int
    ) -> list[Tuple[int, int]]:
        n, m = self.modified_bezout(a, b, c)
        candidates = []
        self.counter += 1
        if n <= 0 and m <= 0:
            return candidates

        d = gcd(a, b)

        # shift through solutions until n is < 0 and m > 0
        self.counter += 1
        if not (n <= 0 and m > 0):
            self.counter += 1
            while n > 0:
                self.counter += 1
                n -= b // d
                m += a // d

        self.counter += 1
        while m - (a // d) > 0:
            self.counter += 1
            n += b // d
            m -= a // d
            candidates.append((n, m))

        return candidates


def main(argv: list[str]):
    if len(argv) < 4:
        print(
            "Not enough arguments. This program expects 3 command line inputs,"
            + " s, x, and y, as strings of 0's and 1's."
        )

    weaving = Interweaving(argv[1], argv[2], argv[3])
    if weaving.is_interweaving():
        print(
            f"Success! {argv[1]} is an interweaving of {argv[2]} and {argv[3]}"
        )
    else:
        print("Could not determine if this is an interweaving")


if __name__ == "__main__":
    main(sys.argv)
