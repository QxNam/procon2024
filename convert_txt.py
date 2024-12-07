import json

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
        general = data.get('general',{})
        if general:
            f.write(f"{general['n']}\n")
            for pattern in general['patterns']:
                f.write(f"{pattern['p']} {pattern['width']} {pattern['height']}\n")
                for row in pattern['cells']:
                    f.write("".join(map(str, row)) + "\n")

# Đọc dữ liệu JSON
with open("input.json", "r") as file:
    data = json.load(file)

# Lưu dữ liệu gốc vào file input_row.txt
save_original_data(data, "input_row.txt")

print("The original data has been saved to 'input_row.txt'.")

