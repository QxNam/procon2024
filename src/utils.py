import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os
import imageio
import json
from time import time
PWD = os.path.dirname(os.path.realpath(__file__))
loaded_data = np.load(f'{PWD}/states/pattents.npz')

def _choose(id:int=0):
    '''
    Parse die in numpy format
    Args:
        id (int): the id of the die
    Returns:
        np.ndarray: the die
    '''
    return loaded_data['arr_{}'.format(id)]

def load_dies():
    '''
    Load all dies default
    Returns:
        list: list of np.ndarray
    '''
    return [_choose(i) for i in range(25)]

def get_point(game: np.ndarray, die: np.ndarray, x: int, y: int) -> tuple:
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

def lift_elements(A: np.ndarray, die: np.ndarray):
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

def apply_die_cutting(board: np.ndarray, pattent: np.ndarray, x: int, y: int, d: int):
    '''
    Cut the die in the game
    Args:
        board (np.ndarray): the board game
        pattent (np.ndarray): the pattent
        x (int): the x coordinate
        y (int): the y coordinate
        d (int): the d (0-top, 1-bottom, 2-left, 3-right)
    Returns:
        np.ndarray: the new board game
    '''
    game = board.copy()
    die = pattent.copy()
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

def load_solution(id):
    with open(f"{PWD}/solves/{id}.json", "r", encoding='utf-8') as f:
        solve = json.load(f)
    return solve

def load_data(id):
    '''
    Load the data from the json file
    Args:
        id (int): the id of the data
    Returns:
    dict: the data loaded from the json file
    '''
    with open(f'{PWD}/data/{id}.json', 'r') as f:
        data = json.load(f)
    data['board'] = np.array(data['board'])
    data['goal'] = np.array(data['goal'])
    data['w'] = data['w']
    data['h'] = data['h']
    dies = load_dies()
    if len(data['dies']) > 0:
        data['dies'] = dies + [np.array(i) for i in data['dies']]
    else:
        data['dies'] = dies
    return data

def save_figure(id, state:np.ndarray=None, goal:np.ndarray=None, step=0, title=None, show=False, folder='figures'):
    '''Save figure at src/figures
    Args:
        id (int): ID of the problem
        state (np.ndarray): Current state
        goal (np.ndarray): Goal state
        step (int): Step of the solution
        show (bool): Show the figure
        folder (str): Folder to save the figure
    '''
    PATH = f'{PWD}/{folder}/{id}' if folder else f'{PWD}/{id}'
    os.makedirs(PATH, exist_ok=True)
    if state is None and goal is None:
        data = load_data(id)
        state = data['board']
        goal = data['goal']
    check = state == goal
    score = np.sum(check.astype(int))
    cmap = ListedColormap(['red', 'green'])
    plt.imshow(check.astype(int), cmap=cmap, vmin=0, vmax=1)
    plt.xticks([])
    plt.yticks([])
    if title is None:
        plt.title(f'ID {id} - Step {step} - Score {score/np.prod(check.shape):.2%}')
    else:
        plt.title(title)
    if show:
        plt.show()
    else:
        plt.savefig(f'{PATH}/{step}.png', bbox_inches='tight')
    plt.close()

def create_gif(id, source_path='figures', gif_path='gifs', duration=0.5):
    '''
    Create GIF from images in the specified folder
    Args:
        id (int): ID of the problem
        source_path (str): Folder containing images
        gif_path (str): Folder to save the GIF
        duration (float): Duration for each frame
    '''
    folder = f'{PWD}/{source_path}/{id}'
    OUTPUT = f'{PWD}/{gif_path}'
    os.makedirs(OUTPUT, exist_ok=True)
    images = []
    for file_name in sorted(os.listdir(folder)):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            images.append(imageio.imread(os.path.join(folder, file_name)))
    imageio.mimsave(f'{OUTPUT}/{id}.gif', images, duration=duration)

def visualize(id, gif=False):
    data = load_data(id)
    state = data['board'].copy()
    goal = data['goal'].copy()
    dies = data['dies']
    solve = load_solution(id)
    for step, meta in enumerate(solve["answer_data"]["ops"]):
        p, x, y, s = meta['p'], meta['x'], meta['y'], meta['s']
        state = apply_die_cutting(state, dies[p], x, y, s)
        save_figure(id, state, goal, step+1, show=False)
    if gif:
        create_gif(id)

def estimate_time(func, **kwargs):
    '''
    Estimate the time of the function
    Args:
        func (function): the function to estimate the time of
        **kwargs: the arguments for the function
    Returns:
        tuple: the time second (s) and the result of the function
    '''
    start = time()
    res = func(**kwargs)
    return time()-start, res
    
def create_json_submit(id:int, results:list):
    '''
    Create the json file for submitting the answer
    Args:
        id (int): the id of the data
        results (list): the results
    '''
    data = {
        "question_id": id,
        "answer_data": {
            "n": len(results),
            "ops": results
        }
    }
    with open(f'{PWD}/solves/{id}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
