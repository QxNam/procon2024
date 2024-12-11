from utils import apply_die_cutting, load_data, apply_die_cutting, visualize, save_figure, create_json_submit
import sys
from time import time
import itertools
import argparse

def get_one_dies(dies, max_size=None):
    '''Lấy các dies toàn số 1'''
    if max_size:
        return {i: dies[i].shape[0] for i in [0, 1, 4, 7, 10, 13, 16, 19, 22] if dies[i].shape[0] <= max_size}
    return {i: dies[i].shape[0] for i in [0, 1, 4, 7, 10, 13, 16, 19, 22]}

def get_alternate_dies(dies, max_size=None):
    '''Lấy các dies so le 0-1'''
    exclude = get_one_dies(max_size)
    return {i:dies[i].shape[0] for i in range(len(dies)) if i not in exclude and dies[i].shape[0] <= max_size}

def get_dies_by_size(dies, size):
    '''Lấy các dies giới hạn theo kích thước'''
    return {i: dies[i].shape for i in range(len(dies)) if min(dies[i].shape) <= size}

def get_direction(check):
    '''lấy các hướng có thể dùng cho state'''
    direction = [0, 1, 2, 3] # top, bot, left, right
    if check[0,:].all():
        direction.remove(1)
    if check[-1,:].all():
        direction.remove(0)
    if check[:,0].all():
        direction.remove(3)
    if check[:,-1].all():
        direction.remove(2)
    return direction

def get_points(check):
    '''lấy tọa độ điểm đầu và cuối của vùng đã đi'''
    h, w = check.shape
    start_x, start_y, end_x, end_y = 0, 0, w, h
    for y in range(h):
        if not check[y, :].all():
            start_y = y
            break
    for y in range(h-1, -1, -1):
        if not check[y, :].all():
            end_y = y
            break
    for x in range(w):
        if not check[:, x].all():
            start_x = x
            break
    for x in range(w-1, -1, -1):
        if not check[:, x].all():
            end_x = x
            break
    return [(start_x, start_y), (end_x, end_y)]


def search_with_thresh(board, goal, n_dies=1, n_steps=3):
    max_score = board.size
    thresh = 0
    results = []
    state = board.copy()
    size = max(state.shape)
    for step in range(n_steps):
        s_time = time()
        check = state == goal
        directions = get_direction(check) # lấy các hướng có thể dùng cho state
        xy_start, xy_end = get_points(check)
        x_start, y_start = xy_start
        x_end, y_end = xy_end
        step_score = sum(check.astype(int).flatten())
        thresh = step_score/max_score
        max_state = state.copy()
        step_result = None
        for x in range(x_start, x_end+1):
            for y in range(y_start, y_end+1):
                die_idxs = get_dies_by_size(dies, max(x_end-x_start+1, y_end-y_start+1))
                for id_die in die_idxs:
                    for direction in directions:
                        new_state = apply_die_cutting(state, dies[id_die], x, y, direction)
                        new_thresh = sum((new_state==goal).astype(int).flatten())/max_score
                        if new_thresh > thresh:
                            thresh = new_thresh
                            max_state = new_state.copy()
                            step_result = {'p': id_die, 'x': x, 'y': y, 's': direction}
                        progress_info = f"Step {step+1}: Correct percent {new_thresh:.2f}"
                        print('\r' + progress_info, end='')
                        sys.stdout.flush()
        print('\r' + f"\n🟢 Step {step+1}: Correct percent {thresh:.2f} - Output {step_result} - Time: {time()-s_time:.2f}s")
        state = max_state.copy()
        if step_result is not None:
            results.append(step_result)
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="1 dies, n_move")
    parser.add_argument("--id", type=int, required=True, help="The ID of the question")
    args = parser.parse_args()
    _id = args.id
    data = load_data(_id)
    board = data['board'].copy()
    goal = data['goal'].copy()
    dies = data['dies']
    w = data['w']
    h = data['h']

    results = search_with_thresh(board, goal)
    create_json_submit(_id, results)
    visualize(_id, True)