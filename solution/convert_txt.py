import json
import argparse

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

if __name__ == "__main__":
    args = parser.parse_args()
    question_id = args.question_id
    
    # Đọc dữ liệu JSON
    with open(f"data\input_{question_id}.json", "r") as file:
        data = json.load(file)

    # Lưu dữ liệu gốc vào file input_row.txt
    save_data(data, f"data\input_{question_id}.txt")
    print(f"The original data has been saved to 'input_{question_id}.txt'.")

