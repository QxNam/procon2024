import json
import argparse
from colorama import Fore, Style, init
import matplotlib.pyplot as plt
import numpy as np


init()

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--question_id", type=int, required=True, help="ID question cần nhập vào")

# Hàm lưu dữ liệu gốc vào file
def save_data(data, filename):
    with open(filename, "w") as f:
        # BOARD
        board = data['board']
        f.write(f"{board['width']} {board['height']}\n")
        for row in board['start']:
            f.write("".join(map(str, row)) + "\n")
        for row in board['goal']:
            f.write("".join(map(str, row)) + "\n")

        # GENERAL
        general = data.get('general',{})
        if general:
            f.write(f"{general['n']}\n")
            for pattern in general['patterns']:
                f.write(f"{pattern['p']} {pattern['width']} {pattern['height']}\n")
                for row in pattern['cells']:
                    f.write("".join(map(str, row)) + "\n")
                    
# Hàm hiển thị ma trận với matplotlib và lưu ảnh
def visualize_matrices(start, goal, output_path):
    start = np.array(start)
    goal = np.array(goal)

    # Tạo ma trận màu: Xanh lá cây nếu giống nhau, đỏ nếu khác nhau
    diff_matrix = np.where(start == goal, 1, 0)  # 1: Giống nhau, 0: Khác nhau

    # Tạo hình vẽ
    height, width = len(start), len(start[0])
    fig, ax = plt.subplots(figsize=(width / 32 * 5, height / 32 * 5))
    for i in range(len(start)):
        for j in range(len(start[i])):
            color = "green" if start[i][j] == goal[i][j] else "red"
            ax.text(j, i, str(start[i][j]), ha="center", va="center", color=color, fontsize=12)

    # Hiển thị ma trận diff_matrix để nền hình ảnh rõ hơn
    ax.imshow(diff_matrix, cmap="Greens", interpolation="none", alpha=0.3)

    # Cài đặt lưới và nhãn
    ax.set_xticks(range(len(start[0])))
    ax.set_yticks(range(len(start)))
    ax.set_xticklabels(range(len(start[0])), rotation=90, ha="center")
    ax.set_yticklabels(range(len(start)))
    ax.set_title("Matrix Visualization (Green: Same, Red: Different)")

    plt.tight_layout()
    # Lưu hình ảnh vào file
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    args = parser.parse_args()
    question_id = args.question_id
    
    # Đọc dữ liệu JSON
    with open(f"data\input\input_{question_id}.json", "r") as file:
        data = json.load(file)
        
    start = data['board']['start']
    goal = data['board']['goal']
    output_path = f"data\input\input_{question_id}.png" 
    # visualize_matrices(start, goal, output_path)                                              ### 

    # Lưu dữ liệu gốc vào file input_row.txt
    save_data(data, f"data\input\input_{question_id}.txt")
    print(f"The original data has been saved to 'data\input\input_{question_id}.txt'.")

