import time
import numpy as np
from die_cutting import apply_die_cutting, _choose
import requests
import time 
import multiprocessing

PROCON_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQsIm5hbWUiOiJEdW1wbGluZ0NvZGUiLCJpc19hZG1pbiI6ZmFsc2UsImlhdCI6MTczMjM0MjMyNiwiZXhwIjoxNzMyNTE1MTI2fQ.gccLdfTQaHcj9OqCxrM8LRS8DjKngam2FTVYksW31K8'
url = "https://proconvn.duckdns.org"
headers = {"Authorization": PROCON_TOKEN}
question_id = 70
question = requests.get(f"{url}/question/{question_id}", headers=headers).json()


def process_direction(data):
    
    start_matrix, goal_matrix, die_patterns, direction = data
    h_board, w_board = start_matrix.shape
    h_die, w_die = list(die_patterns.values())[0].shape
    max_i = w_die + w_board + 1
    max_j = h_die + h_board + 1

    for matrix_id, die_pattern in die_patterns.items():
        for i in range(max_i):
            for j in range(max_j):
                temp_matrix = start_matrix.copy()
                apply_die_cutting(temp_matrix, die_pattern, i, j, direction)
                if np.array_equal(temp_matrix, goal_matrix):
                    return {
                        "n": 1,
                        "ops": [{"p": matrix_id, "x": i, "y": j, "s": direction}]
                    }
    return None

def find_die_and_move_lr_parallel_direction(start_matrix, goal_matrix):
    start_time = time.time()
    die_patterns = {matrix_id: _choose(matrix_id) for matrix_id in range(12, 25)}
    directions = [0, 1, 2, 3]
    task_data = [(start_matrix, goal_matrix, die_patterns, direction) for direction in directions]

    with multiprocessing.Pool(processes=4) as pool: 
        results = pool.map(process_direction, task_data)

    for result in results:
        if result is not None:
            elapsed_time = time.time() - start_time
            print(f"time: {elapsed_time:.2f} seconds")
            return result

    return None
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    data = eval(question.get('question_data'))
    start_matrix = np.array(data["board"]["start"])
    goal_matrix = np.array(data["board"]["goal"])
    sol = find_die_and_move_lr_parallel_direction(start_matrix, goal_matrix)
    print(sol)
