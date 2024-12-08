from states.utils import apply_die_cutting, load_data, estimate_time, save_figure, load_dies
from sol_2die_2move_type_die import find_corners_numpy

def sol_3(h, w, board, goal, dies): # 2 die 2 moves dựa trên ngưỡng
    max_score = np.sum(board!=goal)
    results= []
    top, left, _, _ = find_corners_numpy(board, goal)[0]
    for x in range(left, w):
        for y in range(top, h):
            for d in [0,2,3]: #có thể đổi hướng dựa trên vis
                for id, die in enumerate(dies):
                    new_state = apply_die_cutting(board, die, x, y, d)
                    score = np.sum(new_state!=goal)
                    if (score-max_score)/max_score <= -0.6: 
                        results.append((id, x, y, d))
                        top2, left2, _, _ = find_corners_numpy(new_state, goal)[0]
                        for x2 in range(left2, w):
                            for y2 in range(top2, h):
                                for d2 in [3,2]:  #có thể đổi hướng dựa trên vis
                                    for id2, die2 in enumerate(dies):
                                        new_state2 = apply_die_cutting(new_state, die2, x2, y2, d2)
                                        score2 = np.sum(new_state2!=goal)
                                        if score2==0:
                                            results.append((id2, x2, y2, d2))
                                            return results
                                            
                                    
    # return results

