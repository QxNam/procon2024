from utils import load_data, save_figure, create_json_submit, apply_die_cutting, estimate_time
import numpy as np

def solve_72(h, w, board, goal, dies):
    y_start = 0
    for i in range(h):
        check = board == goal
        if not np.all(check[i]):
            y_start = i
            break

    for y in range(y_start, h):
        for x in range(0, w):
            for id, die in enumerate(dies):
                for d in [0, 2, 3]:
                    state = apply_die_cutting(board, die, x, y, d)
                    if np.all(state == goal):
                        return [{
                            'p': id,
                            'x': x,
                            'y': y,
                            's': d
                        }]
                    
def solve_70(h, w, board, goal, dies):
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

    # full block first
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


                        # full table
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

if __name__ == '__main__':
    question_id = 70
    data = load_data(question_id)
    second, results = estimate_time(solve_70, **{'h': data['h'], 'w': data['w'], "board": data['board'], "goal": data['goal'], "dies": data['dies']})
    print(f'⌛️ {second} seconds')
    state = data['board'].copy()
    for result in results:
        state = apply_die_cutting(state, data['dies'][result['p']], result['x'], result['y'], result['s'])

    save_figure(question_id, state, data['goal'], False)
    create_json_submit(question_id, results)