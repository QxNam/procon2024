import numpy as np
from utils import save_json

def create_die(n:int, type='I') -> list[str]:
    '''
    Create a die with (n x n) cells

    Args:
        n (int): Number of cells in the die
        type (str): Type of the die (I, II, III)

    Returns:
        list: A list of strings representing the die cells, where each cell is represented by a string of '0's and '1's
    '''
    if n==1:
        return np.ones(n, dtype=np.int8).astype(str).tolist()
    
    die = np.ones((n, n), dtype=np.int8)
    if type == 'II':
        die[1::2] = 0
    elif type == 'III':
        die[:,1::2] = 0
    die = die.astype(str).tolist()
    die = [''.join(row) for row in die]
    return die

def create() -> dict:
    '''
    Create a dictionary containing the cell data and save it as a JSON file
    
    Returns:
        dict_cell: A dictionary containing the cell data
    '''
    cell = {}
    p = 0
    n = 1, 2, 4, 8, 16, 32, 64, 128, 256
    dies = [1, 2, 4, 8, 16, 32, 64, 128, 256]

    for n in dies[:]:
        for type in ['I', 'II', 'III']:
            cell[p] = create_die(n, type=type)
            p += 1
            if n == 1:
                break
    return cell

if __name__ == '__main__':
    cells = create()
    save_json('cells', cells)