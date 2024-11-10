import argparse
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from numpy import ndarray
try:
    from .get_problem import getProblem
except ImportError:
    from get_problem import getProblem


def plotQuestion(question_id:int, save:bool=False):
    data = getProblem(question_id)
    if data is None:
        return
    h = data.get('height')
    w = data.get('width')
    start = data.get('start')
    goal = data.get('goal')

    if isinstance(start, list):
        start = np.array(start)
    if isinstance(goal, list):
        goal = np.array(goal)
    if start.shape != goal.shape:
        raise ValueError("Matrices must have the same dimensions.")

    comparison_matrix = (start == goal).astype(int)
    if save:
        plt.savefig(f"question_store/{question_id}.png")
    sns.set_theme(rc={'figure.figsize': (w, h)})
    sns.heatmap(comparison_matrix, cmap="RdYlGn", fmt="d", cbar=False)
    plt.show()

    return comparison_matrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a question ID.")
    parser.add_argument("--question_id", type=int, required=True, help="The ID of the question")
    #saveimage
    parser.add_argument("--save_image", type=bool, default=False, help="Save image to question_store")
    args = parser.parse_args()
    question_id = args.question_id
    save_image = args.save_image
    plotQuestion(question_id=question_id, save=save_image)