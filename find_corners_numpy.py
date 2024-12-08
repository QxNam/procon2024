import numpy as np
from scipy.ndimage import label

def find_corners_numpy(matrix1, matrix2):
    matrix1 = np.array(matrix1)
    matrix2 = np.array(matrix2)
    # sửa thành code tìm tọa độ của vùng liên thông lớn nhất
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
