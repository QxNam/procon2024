import sys
from pathlib import Path

# Thêm thư mục gốc (tức là thư mục chứa utils.py) vào sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils import apply_die_cutting


import numpy as np

board = np.array([
    [1, 0, 1, 1, 2, 2, 1],
    [2, 3, 1, 1, 0, 0, 2],
    [3, 0, 2, 1, 1, 1, 1],
    [3, 0, 0, 2, 2, 3, 1],
    [2, 2, 3, 2, 0, 2, 2],
    [3, 3, 1, 0, 3, 2, 3]
])

print(board.shape) # row, col == h, w

die = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [1, 1, 0]
])

apply_die_cutting(board, die, 0, 0, 2)
print(board)