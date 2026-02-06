
def is_safe(board, row, col, n):
    """
    Checks if placing a queen at (row, col) is safe against previously placed queens.
    board: 1D list where board[r] = c means a queen is at (r, c).
           If board[r] == -1, no queen is there.
    """
    # Check this row on left side - No need, we are placing one per row
    
    # Check valid rows from 0 to row-1
    for i in range(row):
        existing_col = board[i]
        
        # Same column check
        if existing_col == col:
            return False
            
        # Diagonals check
        # Abs difference of rows == Abs difference of cols means diagonal
        if abs(i - row) == abs(existing_col - col):
            return False
            
    return True
