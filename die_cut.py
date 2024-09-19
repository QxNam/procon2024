import numpy as np
from pprint import pprint
from utils import list_to_matrix, check_goal, load_json

def apply_die_cut(board:np.ndarray, die:np.ndarray, x:int, y:int, s:int) -> np.ndarray:
    '''
    Apply die cut to the board

    Args:
        board (numpy.ndarray): The current board state
        die (numpy.ndarray): The die to be cut
        x (int): The x-coordinate of the top-left corner of the die cut
        y (int): The y-coordinate of the top-left corner of the die cut
        s (int): The direction of the die cut (0-top, 1-bottom, 2-left, 3-right)

    Returns:
        numpy.ndarray: The updated board state after applying the die cut

    '''
    # print(die)
    # Get die dimensions
    die_rows, die_cols = die.shape

    # Apply die cut based on direction 's'
    if s == 0:  # Cut from top
        # Ensure the die fits on the board starting from (x, y)
        if x + die_rows > board.shape[0] or y + die_cols > board.shape[1]:
            raise ValueError("Die cut exceeds board boundaries.")
        # Subtract die from the board
        board[x:x + die_rows, y:y + die_cols] -= die

    elif s == 1:  # Cut from bottom
        # Ensure the die fits on the board starting from the bottom
        if x - die_rows < 0 or y + die_cols > board.shape[1]:
            raise ValueError("Die cut exceeds board boundaries.")
        # Subtract die from the board (starting from bottom)
        board[x - die_rows:x, y:y + die_cols] -= die

    elif s == 2:  # Cut from left
        # Ensure the die fits on the board starting from the left
        if x + die_rows > board.shape[0] or y + die_cols > board.shape[1]:
            raise ValueError("Die cut exceeds board boundaries.")
        # Subtract die from the board starting from the left side
        board[x:x + die_rows, y:y + die_cols] -= die

    elif s == 3:  # Cut from right
        # Ensure the die fits on the board starting from the right
        if x + die_rows > board.shape[0] or y - die_cols < 0:
            raise ValueError("Die cut exceeds board boundaries.")
        # Subtract die from the board starting from the right side
        board[x:x + die_rows, y - die_cols:y] -= die

    # Ensure no negative values in the board (cut is binary: cut or not cut)
    board[board < 0] = 0

    # Convert the board back to the list of strings
    board = ["".join(map(str, row)) for row in board]
    return board