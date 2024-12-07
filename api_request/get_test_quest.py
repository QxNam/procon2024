import requests
import json
import argparse

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--id", type=int, required=True, help="ID cần nhập vào")

def get_test(id:int) ->dict:
    url_request = f"http://192.168.1.3:8010/get_data/?id={id}"
    data = requests.get(url_request)
    final_data = {}
    final_data['board'] = data.json()
    file_path = "input.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(final_data, file, ensure_ascii=False, indent=4)

    print(f"Dữ liệu đã được lưu vào tệp {file_path}")
    
if __name__ == "__main__":
    args = parser.parse_args()
    id = args.id 
    get_test(id)