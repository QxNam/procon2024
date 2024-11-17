import json
import numpy as np
from pprint import pprint

class Question:
    def __init__(self, src):
        pass

def get_questions(path:str) -> dict:
    with open(path, 'r') as f:
        response = json.load(f)
    return {
        'response': response,
        'data': json.loads(response.get('question_data'))
    }

if __name__ == '__main__':
    data = get_questions('66.json')
    # pprint(data['data'].keys())
    # board = np.array(data['data']['board']['start'])
    # goal = np.array(data['data']['board']['goal'])
    # print(board.shape, goal.shape)
    dies = [np.array(dict_data['cells']) for dict_data in data['data']['general']['patterns']] # 'width' -> col, 'height' -> row
    print(dies[0].shape)
    print(len(dies[0]))