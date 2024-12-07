import requests
import json
import argparse

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--question_id", type=int, required=True, help="ID cần nhập vào")
parser.add_argument("--user_id", type=str, required=True, help="ID cần nhập vào")


def submit_anwer(user_id :str, question_id:int):
    url_request = f"http://192.168.1.3:8010/submit_answer"
    submit_data = {}
    with open("output.json", 'r') as file:
        ans_data = json.load(file)
    if ans_data:
        submit_data["user_id"] = user_id
        submit_data["question_id"] = question_id
        submit_data["answer_data"] = ans_data
    
    requests.post(url_request, json= submit_data)

if __name__ == "__main__":
    args = parser.parse_args()
    user_id = args.user_id
    question_id = args.question_id 
    submit_anwer(user_id,question_id)
        
    