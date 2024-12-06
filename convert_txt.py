import json

# Hàm chuyển vị ma trận
def transpose_matrix(matrix):
    return list(map(list, zip(*matrix)))

# Hàm hoán đổi height và width
def swap_dimensions(data):
    data['board']['width'], data['board']['height'] = data['board']['height'], data['board']['width']
    for pattern in data['general']['patterns']:
        pattern['width'], pattern['height'] = pattern['height'], pattern['width']

# Hàm lưu dữ liệu gốc vào file
def save_original_data(data, filename):
    with open(filename, "w") as f:
        # BOARD
        board = data['board']
        f.write(f"{board['width']} {board['height']}\n")
        for row in board['start']:
            f.write("".join(map(str, row)) + "\n")
        for row in board['goal']:
            f.write("".join(map(str, row)) + "\n")

        # GENERAL
        general = data['general']
        f.write(f"{general['n']}\n")
        for pattern in general['patterns']:
            f.write(f"{pattern['p']} {pattern['width']} {pattern['height']}\n")
            for row in pattern['cells']:
                f.write("".join(map(str, row)) + "\n")

# Hàm lưu dữ liệu chuyển vị vào file
def save_transposed_data(data, filename):
    with open(filename, "w") as f:
        # BOARD
        board = data['board']
        f.write(f"{board['width']} {board['height']}\n")
        for row in transpose_matrix(board['start']):
            f.write("".join(map(str, row)) + "\n")
        for row in transpose_matrix(board['goal']):
            f.write("".join(map(str, row)) + "\n")

        # GENERAL
        general = data['general']
        f.write(f"{general['n']}\n")
        for pattern in general['patterns']:
            f.write(f"{pattern['p']} {pattern['width']} {pattern['height']}\n")
            for row in transpose_matrix(pattern['cells']):
                f.write("".join(map(str, row)) + "\n")

# Đọc dữ liệu JSON
with open("input.json", "r") as file:
    data = json.load(file)

# Lưu dữ liệu gốc vào file input_row.txt
save_original_data(data, "input_row.txt")

# Swap dimensions (height <-> width) và lưu dữ liệu chuyển vị vào file input_col.txt
swap_dimensions(data)
save_transposed_data(data, "input_col.txt")

print("The original data has been saved to 'input_row.txt'.")
print("The transposed data has been saved to 'input_col.txt'.")

