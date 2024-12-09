import requests
import json
import argparse
import dotenv
import os

url = f"https://proconvn.duckdns.org"
url = f"https://procon.iuhkart.systems"             # nhớ sửa lại PROCON_TOKEN trong .env trong get_test_quest và post_test_quest 
dotenv.load_dotenv()
PROCON_TOKEN = os.environ.get('PROCON_TOKEN', "UNKNOWN")
HEADER = {"Authorization": PROCON_TOKEN}

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--question_id", type=int, required=True, help="ID cần nhập vào")


def submit_anwer(question_id:int):
    url_request = url + f"/answer"
    print('POST: ', url_request)
    submit_data = {}
    submit_data["question_id"] = question_id
    with open(f"data\output\output_{question_id}.json", 'r') as file:
        ans_data = json.load(file)
    if ans_data:
        submit_data["answer_data"] = ans_data
    
    response = requests.post(url_request, json= submit_data, headers=HEADER)
    if response.status_code==200:
        answer_id = response.json().get('id')
        response_answer = requests.get(f"{url_request}/{answer_id}", headers=HEADER)
        print(response_answer.json().get('score_data'))
    else:
        print("Error submit!")
        print(response.json())
        
def submit_anwer_test(question_id:int):
    url_request = url + f"/answer"
    print('POST: ', url_request)
    submit_data = {}
    submit_data["question_id"] = question_id
    with open(f"data\output\output_{question_id}.json", 'r') as file:
        ans_data = json.load(file)
    if ans_data:
        submit_data["answer_data"] = ans_data
    
    response = requests.post(url_request, json= submit_data, headers=HEADER)
    if response.status_code==200:
        response_answer = requests.get(f"{url_request}/{question_id}", headers=HEADER)
        print(response_answer.json())
    else:
        print("Error submit!")
        print(response.json())
    

if __name__ == "__main__":
    args = parser.parse_args()
    question_id = args.question_id 
    if url == "https://proconvn.duckdns.org":
        submit_anwer(question_id)
    else: 
        submit_anwer_test(question_id)
        
    