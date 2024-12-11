import requests
import json
import argparse
import dotenv
import os

# url = f"https://proconvn.duckdns.org"
# url = f"https://procon.iuhkart.systems"              # nhớ sửa lại PROCON_TOKEN trong .env trong get_test_quest và post_test_quest 
url = f'http://192.168.191.11:8000'
dotenv.load_dotenv()
PROCON_TOKEN = os.environ.get('PROCON_TOKEN', "UNKNOWN")
HEADER1 = {"Authorization": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQsIm5hbWUiOiJEdW1wbGluZ0NvZGUiLCJpc19hZG1pbiI6ZmFsc2UsImlhdCI6MTczMzg5MzU1MSwiZXhwIjoxNzM0MDY2MzUxfQ.nsEJkRlH1AU8CkU9QdYXN1f_WxrRzEyLGLrz0vHCvmQ'}
HEADER2 = {"Authorization": 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRhaXRydW9uZyIsImV4cCI6MTczMzk3MDMzNywic3ViIjoidGFpdHJ1b25nIn0.vvipgStwdsqq6YIx2jc06lmd0c-Ge8Phlz4ZYd7yY9U'}
HEADER3 = {"Authorization": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MzcsIm5hbWUiOiJJVUguUHJvZ3JhbW1pbmdfTGFiIiwiaXNfYWRtaW4iOmZhbHNlLCJpYXQiOjE3MzM5MDA5NDUsImV4cCI6MTczNDA3Mzc0NX0.XmCuJK6dQJKfERdRGMnghKzYO-hbPJyrZFfbZlwuuJY'}
HEADER = HEADER1

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--question_id", type=int, required=True, help="ID question cần nhập vào")

def get_origin_problem(question_id:int) ->dict:
    url_request = url + f"/question/{question_id}"
    print('GET: ', url_request)
    data = requests.get(url_request, headers=HEADER)
    if data.status_code == 200:
        print(f"\033[32mSuccess! HTTP Status Code: {data.status_code}\033[0m")
        if data.json():
            final_data = data.json().get('question_data')
            os.makedirs("./data", exist_ok=True)
            os.makedirs("./data/input", exist_ok=True)
            final_data = eval(final_data)
            file_path = f"./data/input/input_{question_id}.json"
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(final_data, file, ensure_ascii=False, indent=4)
                print(f"Dữ liệu đã được lưu vào tệp {file_path}")
    else:
        print(f"\033[31mError! HTTP Status Code: {data.status_code}\033[0m")  # Màu đỏ
        print(data.json())
        print("\033[31mError when get file\033[0m")
        
def get_test(question_id:int) ->dict:
    url_request = url + f"/question/{question_id}"
    print('GET: ', url_request)
    data = requests.get(url_request, headers=HEADER)
    if data.status_code == 200:
        print(f"\033[32mSuccess! HTTP Status Code: {data.status_code}\033[0m")
        data = data.json()
        os.makedirs("./data", exist_ok=True)
        os.makedirs("./data/input", exist_ok=True)
        final_data={}
        final_data['board'] = data
        final_data['general'] = {
            'n': 0,
            'patterns': []
        }
        file_path = f"./data/input/input_{question_id}.json"
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(final_data, file, ensure_ascii=False, indent=4)
            print(f"Dữ liệu đã được lưu vào tệp {file_path}")
    else:
        print(f"\033[31mError! HTTP Status Code: {data.status_code}\033[0m")  # Màu đỏ
        print("\033[31mError when get file\033[0m")
    
if __name__ == "__main__":
    args = parser.parse_args()
    question_id = args.question_id
    if url == f"https://proconvn.duckdns.org":
        HEADER=HEADER1
        get_origin_problem(question_id)
    elif url == f'http://192.168.191.11:8000':
        HEADER=HEADER2
        get_origin_problem(question_id)
    else:
        HEADER=HEADER3
        get_test(question_id)