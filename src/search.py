from utils import load_data, save_figure, crate_json_submit, apply_die_cutting, estimate_time
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

if __name__ == '__main__':
    data = load_data(72)
    h, w = data['board'].shape
    second, result = estimate_time(solve_72, **{'h': h, 'w': w, "board": data['board'], "goal": data['goal'], "dies": data['dies']})
    print(f'⌛️ {second} seconds')
    result = result[0]
    state = apply_die_cutting(board=data['board'], pattent=data['dies'][result['p']], x=result['x'], y=result['y'], d=result['s'])
    save_figure(72, state, data['goal'], False)
    crate_json_submit(72, result)