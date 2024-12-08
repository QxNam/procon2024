import requests
import json
import argparse
import dotenv
import os

url = f"https://proconvn.duckdns.org"
dotenv.load_dotenv()
PROCON_TOKEN = os.environ.get('PROCON_TOKEN', "UNKNOWN")
HEADER = {"Authorization": PROCON_TOKEN}

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--question_id", type=int, required=True, help="ID question cần nhập vào")

def get_test(id:int) ->dict:
    url_request = url + f"/question/{id}"
    print(url_request)
    data = requests.get(url_request, headers=HEADER)
    if data.json():
        final_data = data.json().get('question_data')
        os.makedirs("./data", exist_ok=True)
        final_data = eval(final_data)
        file_path = f"./data/input_{id}.json"
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(final_data, file, ensure_ascii=False, indent=4)
            print(f"Dữ liệu đã được lưu vào tệp {file_path}")
    else: 
        print(f"Error when get file")
    
if __name__ == "__main__":
    args = parser.parse_args()
    question_id = args.question_id
    get_test(question_id)