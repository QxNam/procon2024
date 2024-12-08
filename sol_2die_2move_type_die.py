from utils import apply_die_cutting, load_data, estimate_time, save_figure, load_dies, create_json_submit
from find_corners_numpy import find_corners_numpy
import numpy as np
import json
import bisect
import argparse

def solve_2moves(h, w, board, goal, dies):
    x_start = 0
    y_start = 0
    for i in range(w):
        if board[1][i] != goal[1][i]:
            x_start = i
            break
    for i in range(h):
        if board[i][0] != goal[i][0]:
            y_start = i
            break
    results = []
    for y in range(y_start, h):
        for x in range(0, w):
            direcs = [0, 2, 3]
            if x > x_start:
                direcs = [2, 3]
            for idie, die in enumerate(dies):
                for d in direcs:
                    state1 = apply_die_cutting(board, die, x, y, d)
                    if np.all(state1[:, :x_start] == goal[:, :x_start]):
                        results.append({
                            'p': idie,
                            'x': x,
                            'y': y,
                            's': d
                        })

                        for y2 in range(0, h):
                            for x2 in range(x_start, w):
                                for d2 in [0, 1, 2]:
                                    state2 = apply_die_cutting(state1, die, x2, y2, d2)
                                    if np.all(state2 == goal):
                                        results.append({
                                            'p': idie,
                                            'x': x2,
                                            'y': y2,
                                            's': d2
                                        })
                                        return results
                        results = []

def main(id):
    data = load_data(id)
    board = data['board'].copy()
    goal = data['goal'].copy()
    dies = data['dies']
    height = data['h']
    weight = data['w']
    sol = solve_2moves(height, weight, board, goal, dies)
    print(json.dumps(sol, indent=2)) 
    create_json_submit(id, sol)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve the 2-move by ID.')
    parser.add_argument("--id", type=int, required=True, help="The ID of the question")
    
    args = parser.parse_args()
    
    main(args.id)