import json
import numpy as np


def create_dies(n, type='I'):
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

def save_json(filename, data):
    with open(f'data/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def create():
    cell = {}
    p = 0
    n = 1, 2, 4, 8, 16, 32, 64, 128, 256
    dies = [1, 2, 4, 8, 16, 32, 64, 128, 256]

    for n in dies[:]:
        for type in ['I', 'II', 'III']:
            cell[p] = create_dies(n, type=type)
            p += 1
            if n == 1:
                break
    return cell

cells = create()
save_json('cells', cells)