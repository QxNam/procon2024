import numpy as np
from numpy import ndarray
import os
PWD = os.path.dirname(os.path.realpath(__file__))
loaded_data = np.load(f'{PWD}/states/pattents.npz')

def _choose(id:int=1):
    return loaded_data['arr_{}'.format(id)]

def get_dies():
    return [_choose(i) for i in range(24)]

def get_point(game: ndarray, die: ndarray, x: int, y: int) -> tuple:
    '''
    Get the point of the die in the game
    
    Args:
        game (np.ndarray): the game game
        die (np.ndarray): the die
        x (int): the x coordinate
        y (int): the y coordinate
    
    Returns:
        tuple: the x_start, y_start, x_end, y_end
    '''
    h, w = game.shape
    _h, _w = die.shape
    x_end = min(x + _w, w)
    y_end = min(y + _h, h)
    x_start, y_start = max(x, 0), max(y, 0)

    return x_start, y_start, x_end, y_end

def lift_elements(A: ndarray, die: ndarray):
    '''
    Lift the elements of the die in the game
    
    Args:
        A (np.ndarray): the game game
        die (np.ndarray): the die
        
    Returns:
        tuple: the lifted elements and the position of the die
    '''
    h, w = A.shape
    tmp_die = die[:h, :w]
    res = np.zeros(A.shape, dtype=int)-1
    pos_1 = np.where(tmp_die == 1)
    res[pos_1] = A[pos_1]
    return res, pos_1

def apply_die_cutting(board: ndarray, pattent: ndarray, x: int, y: int, d: int)->ndarray:
    '''
    Cut the die in the game

    Args:
        game (np.ndarray): the game game
        pattent (np.ndarray): the pattent
        x (int): the x coordinate
        y (int): the y coordinate
        d (int): the d (0-top, 1-bottom, 2-left, 3-right)
    '''
    die = pattent.copy()
    game = board.copy()
    height, width = game.shape
    if x<0:
        die = die[:, -x:]
    if y<0:
        die = die[-y:, :]

    x1, y1, x2, y2 = get_point(game, die, x, y)
    A = game[y1:y2+1, x1:x2+1]
    
    L, P = lift_elements(A, die)
    P_ = (P[0] + y1, P[1] + x1)
    game[P_] = -1
    if d>1:
        for r in range(y1, y2):
            col1 = [game[r][i] for i in range(width) if game[r][i] != -1]
            col2 = [L[r-y1][i] for i in range(len(L[r-y1])) if L[r-y1][i] != -1]
            if d == 2: # left
                col = np.concatenate((col1, col2))
                game[r] = col
            elif d == 3: # right
                col = np.concatenate((col2, col1))
                game[r] = col
    else:
        for c in range(x1, x2):
            row1 = [game[i][c] for i in range(height) if game[i][c] != -1]
            row2 = [L[i][c-x1] for i in range(len(L)) if L[i][c-x1] != -1]
            if d == 0: # top
                row = np.concatenate((row1, row2))
                game[:, c] = row
            elif d == 1: # bottom
                row = np.concatenate((row2, row1))
                game[:, c] = row
    return game
            