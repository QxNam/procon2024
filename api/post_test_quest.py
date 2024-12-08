import requests
import json
import argparse
import dotenv
import os

dotenv.load_dotenv()
PROCON_TOKEN = os.environ.get('PROCON_TOKEN', "UNKNOWN")
HEADER = {"Authorization": PROCON_TOKEN}
parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--question_id", type=int, required=True, help="ID cần nhập vào")


def submit_anwer(question_id:int):
    url_request = f"http://192.168.1.15:8000/answer"
    submit_data = {}
    with open("output.json", 'r') as file:
        ans_data = json.load(file)
    if ans_data:
        # submit_data["user_id"] = user_id
        submit_data["question_id"] = question_id
        submit_data["answer_data"] = ans_data
    
    response = requests.post(url_request, json= submit_data, headers=HEADER)
    if response.status_code==200:
        print(response.json())
    else:
        print("Error submit!")

if __name__ == "__main__":
    args = parser.parse_args()
    question_id = args.question_id 
    submit_anwer(question_id)
        
    