import numpy as np
from scipy.ndimage import label

def find_corners_numpy(matrix1, matrix2):
    matrix1 = np.array(matrix1)
    matrix2 = np.array(matrix2)
    diff = matrix1 != matrix2
    if not np.any(diff):  return None

    labeled, num_features = label(diff)
    corners = []
    
    for i in range(1, num_features + 1):
        indices = np.argwhere(labeled == i)
        
        top = np.min(indices[:, 0]) 
        bottom = np.max(indices[:, 0])  
        left = np.min(indices[:, 1])  
        right = np.max(indices[:, 1])
        
        new_corners = [top, left, bottom, right]
        
        overlap = False
        for corner in corners:
            prev_top, prev_left, prev_bottom, prev_right = corner
            if not (right < prev_left or left > prev_right or bottom < prev_top or top > prev_bottom):
                overlap = True
                break
        
        if not overlap: corners.append(new_corners)
    
    return corners
def check_type(sub_matrix, sub_matrix_goal):
    lst_col = []
    lst_row = []
    for ci in range(4):
        col_goal_ci = sub_matrix_goal[:,ci]
        for cj in range(sub_matrix.shape[1]):
            if np.array_equal(sub_matrix[:,cj], col_goal_ci):
                lst_col.append(cj)
    for ri in range(4):
        row_goal_ri = sub_matrix_goal[ri]
        for rj in range(sub_matrix.shape[0]):
            if np.array_equal(sub_matrix[rj], row_goal_ri):
                lst_row.append(rj)
    for i in range(len(lst_col)-1):
        if lst_col[i+1] == lst_col[i]+2: 
            return [3, min(lst_col)]
        elif lst_col[i+1] == lst_col[i] +1: 
            return [1, min(lst_col)]
        return 0
    for j in range(len(lst_row)-1):
        if lst_row[j+1] == lst_row[j]+2: 
            return [2, min(lst_row)]
def sol_corner(board, goal):
    corners = find_corners_numpy(board, goal) # sửa cái này lấy vùng liên thông lớn nhất
    w_board = len(board[0])
    results = []
    for i in corners:
        top, left, bottom, right = i
        die_id = max(bottom-top, right-left)
        die_size = [1, 2, 4, 8, 16, 32, 64, 128, 256]
        die_=[die_size[bisect.bisect_right(die_size, die_id) - 1],  die_size[bisect.bisect_left(die_size, die_id)]]
        sub_matrix = board[top:bottom+1, left:right+1]
        sub_matrix_goal = goal[top:bottom+1, left:right+1]
        counts1 = {i: np.sum(sub_matrix == i) for i in range(4)}
        counts2 = {i: np.sum(sub_matrix_goal == i) for i in range(4)}
        if counts1 == counts2:  
            type_die = check_type(sub_matrix, sub_matrix_goal)[0]
            start_x = check_type(sub_matrix, sub_matrix_goal)[1]
            if type_die == 1:
                for d in [1,2,3]:
                    for matrix_id in die_:
                        state= apply_die_cutting(sub_matrix, dies[die_size.index(matrix_id)*3-2], start_x, 0, d)
                        if np.all(state == sub_matrix_goal):  
                            results.append(( die_size.index(matrix_id)*3-2,  start_x+left , top, d))
            elif type_die ==3:
                for d in [1,2,3]:
                    for matrix_id in die_:
                        if left >= w_board//2:
                            state= apply_die_cutting(sub_matrix, dies[die_size.index(matrix_id)*3], start_x-1 , 0, d)
                            if np.all(state == sub_matrix_goal): results.append(( die_size.index(matrix_id)*3,  start_x+left-1 , top, d))
                        else:    
                            state= apply_die_cutting(sub_matrix, dies[die_size.index(matrix_id)*3], start_x , 0, d)
                            w_die = len(dies[die_size.index(matrix_id)*3]) + start_x
                            if np.all(state == sub_matrix_goal) and w_die <= w_board: results.append(( die_size.index(matrix_id)*3,  start_x , top, d))
            else: pass
    return {
        "n": len(results),
        "ops": [{"p": re[0], "x": re[1], "y": re[2], "s": re[3]} for re in results]
    }