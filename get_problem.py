import argparse
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv('.env')
PROCON_TOKEN = os.environ.get('PROCON_TOKEN')


url = "https://proconvn.duckdns.org"
headers = {"Authorization": PROCON_TOKEN}


def getProblem(question_id:int):
    response = requests.get(f"{url}/question/{question_id}", headers=headers).json()
    try:
        id_ = response.get('id')
        question_data = eval(response.get('question_data'))
        height = question_data.get('board').get('height')
        width = question_data.get('board').get('width')
        start = question_data.get('board').get('start')
        goal = question_data.get('board').get('goal')
        n_generated = question_data.get('general', {}).get('n',None)
        general_die = question_data.get('general', {}).get('patterns',[])
        data = {
            "id": id_,
            "height": height,
            "width": width,
            "start": start,
            "goal": goal,
            "n_generated": n_generated,
            "general_die": general_die
        }
        return data 
    except Exception as e:
        print("Wrong question id")
        return None
    
# create main function for py 
if __name__ == "__main__":
    #input question_id
    parser = argparse.ArgumentParser(description="Process a question ID.")
    parser.add_argument("--question_id", type=int, required=True, help="The ID of the question")
    args = parser.parse_args()
    question_id = args.question_id
    print(f"Question ID: {question_id}")
    data = getProblem(question_id)
    if not os.path.exists("question_store"):
        os.makedirs("question_store")
    with open(f"question_store/{question_id}.json", "w") as f:
        json.dump(data, f)
    print(f"Save question {question_id} to question_store/{question_id}.json")