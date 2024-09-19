import json
import numpy as np

def save_json(filename, data) -> None:
    '''
    Save JSON data to data directory by file name
    
    Args:
        filename (str): file name to save
        data (dict): JSON data to save
    '''
    with open(f'data/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_json(filename) -> dict:
    '''
    Load JSON data in data directory by file name
    
    Args:
        filename (str): file name to load
    
    Returns:
        dict: loaded JSON data
    '''
    with open(f'data/{filename}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def list_to_matrix(list_string:list[str]) -> np.ndarray:
    '''
    Convert a list[string] to a numpy matrix

    Args:
        list_string (list[str]): List of strings representing the board cells

    Returns:
        numpy.ndarray: A numpy matrix representing the board cells
    '''
    matrix = np.array([list(row) for row in list_string]).astype(np.int_)
    return matrix

def matrix_to_list(matrix: np.ndarray) -> list[str]:
    '''
    Convert a numpy matrix to a list[string]
    
    Args:
        matrix (numpy.ndarray): A numpy matrix representing the board cells
        
    Returns:
        list[str]: List of strings representing the board cells
    '''
    return ["".join(map(str, row)) for row in matrix]

def check_goal(board: np.ndarray, goal: np.ndarray) -> bool:
    '''
    Check if the current board state matches the goal state
    
    Args:
        board (numpy.ndarray): The current board state
        goal (numpy.ndarray): The goal state

    Returns:
        bool: True if the board matches the goal, False otherwise
    '''
    return np.array_equal(board, goal)