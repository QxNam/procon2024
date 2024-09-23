from procon.create_die import random_die
from procon.create_board import create_board
from procon.die_cut import apply_die_cut
from procon.utils import load_json, list_to_matrix, matrix_to_list, save_json
import os, random, json

def auto(example_folder='1', num_step=1, board_shape=(5, 6), general_config=[]):
    '''
    Auto generation of questions and goal

    Args:
        folder (str, optional): The directory to save the questions. Defaults to '1'.
        num_step (int, optional): The number of steps for the solution. Defaults to 1.
        board_shape (tuple, optional): The shape of the board (row, col). Defaults to (5, 6).
        general_config (list, optional): The general configuration. Defaults to [].
    
    Returns:
        None
    '''
    os.makedirs(f'./example/{example_folder}', exist_ok=True)

    # gen the questions
    board = create_board(*board_shape)
    start = board.copy()
    board = list_to_matrix(board) # convert to maxtrix to process
    height, width = board_shape
    dies = load_json('./data/cells')

    # gen gerenal config
    n = len(general_config)
    general = {
        "n": n,
        "patterns": []
    }
    if n>0:
        for idx, (h, w) in enumerate(general_config, 25):
            cell = random_die(h, w)
            dies[idx] = cell
            general["patterns"].append({
                "p": idx,
                "width": w,
                "height": h,
                "cells": cell
            })
    dies = {int(p): list_to_matrix(dies[p]) for p in dies} # convert to maxtrix to process
    
    # create the solution
    answer = {
        "n": num_step,
        "ops": []
    }
    for _ in range(num_step):
        p = random.choice(list(dies.keys()))
        x = random.randint(-width//2, width)
        y = random.randint(-height//2, height)
        s = random.randint(0, 3)
        answer["ops"].append({
            "p": p,
            "s": s,
            "x": x,
            "y": y
        })
        board = apply_die_cut(board, dies[p], x, y, s)
    goal = matrix_to_list(board)

    # save the question
    question = {
        "board": {
            "width": width,
            "height": height,
            "start": start,
            "goal": goal
        },
        "general": general
    }

    # save question and answer
    question_path = os.path.join(f'./example/{example_folder}', f'question.json')
    answer_path = os.path.join(f'./example/{example_folder}', f'answer.json')
    # with open(question_path, 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(question, indent=4))
    # with open(answer_path, 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(answer, indent=4))
    save_json(question_path, question)
    save_json(answer_path, answer)
    print(f'Successfully generated question and answer in {example_folder}!')


if __name__ == '__main__':
    general_config = [(3, 4), (5, 3)]
    board_shape=(8, 5)
    auto(example_folder='4', board_shape=board_shape, general_config=general_config)