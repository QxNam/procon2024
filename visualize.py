import matplotlib.pyplot as plt

# Hàm đọc ma trận từ file input.txt
def read_input(file_path):
    with open(file_path, 'r') as f:
        data = f.readlines()
    
    width, height = map(int, data[0].strip().split())
    start = [data[i + 1].strip() for i in range(height)]  # Ma trận start (bỏ qua)
    goal = [data[i + 1 + height].strip() for i in range(height)]  # Ma trận goal
    
    return goal

# Hàm đọc ma trận đáp án từ file output.txt
def read_output(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Vẽ đồ thị so sánh hai ma trận
def plot_comparison(goal, output):
    height = len(goal)
    width = len(goal[0])
    
    fig, ax = plt.subplots()
    for i in range(height):
        for j in range(width):
            if goal[i][j] == output[i][j]:
                color = 'green'  # Trùng khớp
            else:
                color = 'red'  # Không khớp
            ax.plot(j, -i, 's', color=color, markersize=15)  # Vẽ ô vuông
    
    ax.set_aspect('equal')
    ax.set_xticks(range(width))
    ax.set_yticks(range(-height, 0))
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-height + 0.5, 0.5)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(False)
    plt.show()

# Main
goal_matrix = read_input("input.txt")  # Đọc ma trận goal từ input.txt
output_matrix = read_output("output.txt")  # Đọc ma trận đáp án từ output.txt
plot_comparison(goal_matrix, output_matrix)