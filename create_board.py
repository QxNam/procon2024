import numpy as np
from utils import save_json

def create_board(w:int, h:int) -> list[str]:
    '''
    Create a new board with random values from the range [0, 3]

    Args:
        w (int): Width of the board
        h (int): Height of the board

    Returns:
        list: A list of strings representing the board cells, where each cell is represented by a string of '0', '1', '2', or '3
    '''
    if w in range(1, 257) and h in range(1, 257):
        board = np.random.randint(0, 4, size=(w, h))
        board = board.astype(str).tolist()
        board = [''.join(row) for row in board]
        return board
    else:
        raise ValueError("Width and height must be between 1 and 256 (inclusive)")

def create_board_dict(w:int, h:int) -> dict:
    '''
    Create a dictionary containing the board data and save it as a JSON file
    
    Args:
        w (int): Width of the board
        h (int): Height of the board

    Returns:
        dict: A dictionary containing the board data
    '''
    dict_board = {
        "board": 
            {
                "width": w,
                "height": h,
                "start": create_board(w, h),
                "goal": create_board(w, h)
            }
    }

    return dict_board

if __name__ == "__main__":
    data = create_board_dict(6, 4)
    save_json('board', data)