import requests
import json
import argparse
import dotenv
import os

url = f"https://proconvn.duckdns.org"
url = f"https://procon.iuhkart.systems"
dotenv.load_dotenv()
PROCON_TOKEN = os.environ.get('PROCON_TOKEN', "UNKNOWN")
HEADER = {"Authorization": PROCON_TOKEN}

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--question_id", type=int, required=True, help="ID question cần nhập vào")

def get_origin_problem(question_id:int) ->dict:
    url_request = url + f"/question/{question_id}"
    data = requests.get(url_request, headers=HEADER)
    if data.json():
        final_data = data.json().get('question_data')
        os.makedirs("./data", exist_ok=True)
        final_data = eval(final_data)
        file_path = f"./data/input_{question_id}.json"
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(final_data, file, ensure_ascii=False, indent=4)
            print(f"Dữ liệu đã được lưu vào tệp {file_path}")
    else: 
        print(f"Error when get file")
        
def get_test(question_id:int) ->dict:
    url_request = url + f"/question/{question_id}"
    data = requests.get(url_request, headers=HEADER)
    if data.status_code == 200:
        data = data.json()
        os.makedirs("./data", exist_ok=True)
        final_data={}
        final_data['board'] = data
        final_data['general'] = {
            'n': 0,
            'patterns': []
        }
        file_path = f"./data/input_{question_id}.json"
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(final_data, file, ensure_ascii=False, indent=4)
            print(f"Dữ liệu đã được lưu vào tệp {file_path}")
    else: 
        print(f"Error when get file")
        print(data.json())
    
if __name__ == "__main__":
    args = parser.parse_args()
    question_id = args.question_id
    print("Submit at ",url)
    if url == "https://proconvn.duckdns.org":
        get_origin_problem(question_id)
    else:
        get_test(question_id)