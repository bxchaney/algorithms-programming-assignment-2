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
    ) -> bool:
        self._set_dp_table(s)
        len_x_k = len(self._x) * (len(s) // len(self._x))
        len_y_k = len(self._y) * (len(s) // len(self._y))

        if len(self._x) + len(self._y) > len(s):
            return False
        for i in range(len_x_k + 1):
            for j in range(len_y_k + 1):
                if i + j > len(s):
                    continue
                if i == 0 and j == 0:
                    self._dp[i][j] = True

                elif i == 0:
                    self._dp[i][j] = (
                        self._dp[i][j - 1]
                        and self._y[(j - 1) % len(self._y)] == s[i + j - 1]
                    )

                elif j == 0:
                    self._dp[i][j] = (
                        self._dp[i - 1][j]
                        and self._x[(i - 1) % len(self._x)] == s[i + j - 1]
                    )

                else:
                    self._dp[i][j] = (
                        self._dp[i - 1][j]
                        and self._x[(i - 1) % len(self._x)] == s[i + j - 1]
                    ) or (
                        self._dp[i][j - 1]
                        and self._y[(j - 1) % len(self._y)] == s[i + j - 1]
                    )

        for row in self._dp:
            print([1 if i else 0 for i in row])
        return self._dp[len(self._x)][len(self._y)]

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
        solution = False
        # Necessary condition to have complete repetitions of x and y
        if len(s) % gcd(len(self._x), len(self._y)) != 0:
            print(len(s) % gcd(len(self._x), len(self._y)))
            return solution
        self.check_substrings(s)
        n, m = self.modified_bezout(len(s), len(self._x), len(self._y))
        print(n, m)
        candidates = self.get_candidate_solutions(
            len(self._x), n, len(self._y), m
        )

        for i, j in candidates:
            print(f"Potential solution at:({len(self._x) * i}, {len(self._y) *j})")
            if self._dp[len(self._x) * i][len(self._y) * j]:
                solution = True
                break

        return solution

    def is_interweaving(self) -> bool:
        return self.check_linear_combinations(self._s)

    def modified_bezout(self, c: int, a: int, b: int) -> Tuple[int, int]:
        print("hello")
        s = 0
        r = b
        old_s = 1
        old_r = a

        while r != 0:
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s

        if b != 0:
            t = (old_r - old_s * a) // b
        else:
            t = 0

        # old_r has the gcd
        return (old_s * (c // old_r), t * (c // old_r))

    def get_candidate_solutions(
        self, a: int, n: int, b: int, m: int
    ) -> list[Tuple[int, int]]:
        candidates = []
        if n <= 0 and m <= 0:
            return candidates

        d = gcd(a, b)

        # shift through solutions until n is < 0 and m > 0
        if not (n <= 0 and m > 0):
            while n > 0:
                n -= b // d
                m += a // d

        while m - (a // d) > 0:
            n += b // d
            m -= a // d
            candidates.append((n, m))

        return candidates


if __name__ == "__main__":
    str1 = "11011"
    str2 = "00"
    str3 = "00011011000001101100"
    # print(Solution.isInterleave(str1, str2, str3))
    # print(is_interwoven(str3, str1, str2))
    weaving = Interweaving(str3, str1, str2)
    print(weaving.is_interweaving())
