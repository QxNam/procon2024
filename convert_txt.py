import json

# Dữ liệu JSON
with open("input.json", "r") as file:
    data = json.load(file)

# Hàm chuyển đổi dữ liệu sang định dạng văn bản
def convert_to_txt(data):
    result = []

    # Phần BOARD
    board = data['board']
    result.append(f"{board['width']} {board['height']}")
    start = [''.join(map(str, row)) if isinstance(row, list) else row for row in board['start']]
    result.extend(start)
    result.extend('')
    goal = [''.join(map(str, row)) if isinstance(row, list) else row for row in board['goal']]
    result.extend(goal)
    result.extend('')

    # Phần GENERAL
    general = data['general']
    result.append(f"{general['n']}")
    for i, pattern in enumerate(general['patterns'], start=1):
        result.append(f"{pattern['p']} {pattern['width']} {pattern['height']}")
        cells = [''.join(map(str, row)) if isinstance(row, list) else row for row in pattern['cells']]
        result.extend(cells)
    return "\n".join(result)

# Chuyển đổi và lưu vào file txt
txt_content = convert_to_txt(data)
with open("input.txt", "w") as f:
    f.write(txt_content)

print("The data has been converted to text format and saved to 'input.txt'.")
