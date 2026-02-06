
import copy

class StateLogger:
    def __init__(self):
        self.logs = []

    def log_state(self, board, row, col, action, description="", metrics=None):
        """
        action: 'try', 'place', 'remove', 'solution'
        """
        # Store a copy of the board logic (assuming 1D for now, but visualiser might want 2D later)
        # We'll store the 1D list [col for row 0, col for row 1, ...]
        # -1 represents no queen
        state = {
            "board": copy.copy(board),
            "current_row": row,
            "current_col": col,
            "action": action,
            "description": description,
            "metrics": metrics or {}
        }
        self.logs.append(state)
