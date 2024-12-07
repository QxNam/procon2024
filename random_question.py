import numpy as np
from states.utils import apply_die_cutting, load_dies
def create_board(h, w):
    if w in range(1, 257) and h in range(1, 257):
        board = np.random.randint(0, 4, size=(h, w))
        return board
    else:
        raise ValueError("Width and height must be between 1 and 256 (inclusive)")
def create_position(h, w):
    if  w in range(1, 257) and h in range(1, 257):
        x, y = np.random.randint(0, max(w,h)), np.random.randint(0,max(h, w))
        return x,y
    else: raise ValueError("x, y must be between 1 and 256 (inclusive)")
def create_direction():
    d= np.random.randint(0,4)
    return d
def create_die():
    id = np.random.randint(0,25)
    die = load_dies()[id]
    return die
def create_board_dict(w, h) :
    x, y = create_position(h, w)
    start = create_board(w, h)
    d = create_direction()
    die = create_die()
    goal = apply_die_cutting(start,die,  x, y, d)
    if np.all(start==goal) == False:
        dict_board = {
                    "id":1, 
                    "h": h,
                    "w": w,
                    "board": start.tolist(),
                    "goal": goal.tolist(),
                    "dies":[[1]]
        }

        return dict_board
    
# if __name__ == "__main__":
#     data = create_board_dict(6, 4)