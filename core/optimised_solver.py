import time

class PureNQueenTimer:
    def __init__(self, n):
        self.n = n
        self.board = [-1] * n

    def solve(self):
        start = time.perf_counter()
        self._backtrack(0)
        end = time.perf_counter()
        return end - start

    def _backtrack(self, row):
        if row == self.n:
            return

        for col in range(self.n):
            if self._is_safe(row, col):
                self.board[row] = col
                self._backtrack(row + 1)
                self.board[row] = -1

    def _is_safe(self, row, col):
        for r in range(row):
            c = self.board[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True
