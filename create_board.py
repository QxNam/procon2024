import numpy as np
import json

def create_board(w, h):
    board = np.random.randint(0, 3, size=(w, h))
    board = board.astype(str).tolist()
    board = [''.join(row) for row in board]
    return board

def create_board_dict(w, h):
    dict_board = {
        "board": 
            {
                "width": w,
                "height": h,
                "start": create_board(w, h),
                "goal": create_board(w, h)
            }
    }

    return dict_board

def save_json(filename, data):
    with open(f'data/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

data = create_board_dict(6, 4)
save_json('board', data)