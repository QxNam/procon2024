from utils import apply_die_cutting, load_data, estimate_time, save_figure, load_dies, create_json_submit
import numpy as np
import json
import bisect
import argparse

def solve_1move(h, w, board, goal, dies):
    y_start = 0
    for i in range(h):
        check = board == goal
        if not np.all(check[i]):
            y_start = i
            break

    for y in range(y_start, h):
        for x in range(0, w):
            for id, die in enumerate(dies):
                for d in [0,1, 2, 3]:
                    state = apply_die_cutting(board, die, x, y, d)
                    if np.all(state == goal):
                        return [{"p": id, "x": x, "y": y, "s": d}]
                        
def main(id):
    data = load_data(id)
    board = data['board'].copy()
    goal = data['goal'].copy()
    dies = data['dies']
    height = data['h']
    weight = data['w']
    sol = solve_1move(height, weight, board, goal, dies)
    print(json.dumps(sol, indent=2)) 
    create_json_submit(id, sol)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve the 1-move by ID.')
    parser.add_argument("--id", type=int, required=True, help="The ID of the question")
    
    args = parser.parse_args()
    
    main(args.id)