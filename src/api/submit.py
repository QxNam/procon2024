import argparse
import json
import os
import requests
from dotenv import load_dotenv
from config import PWD

load_dotenv()
PROCON_TOKEN = os.environ.get('PROCON_TOKEN')
url = "https://proconvn.duckdns.org"
headers = {"Authorization": PROCON_TOKEN}

def submit(question_id):
    with open(f"{PWD}/solves/{question_id}.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    response = requests.post(f"{url}/answer", headers=headers, json=data)
    if response.status_code == 200:
        print(f"✅ Submitted question id: {question_id}")
    else:
        print(f"❌ Failed to submit question {question_id}: {response.status_code}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit a solution.")
    parser.add_argument("--id", type=int, required=True, help="The ID of the question")
    args = parser.parse_args()
    question_id = args.id
    
    submit(question_id)