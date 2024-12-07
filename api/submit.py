import argparse
import json
import os
import requests

PROCON_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQsIm5hbWUiOiJEdW1wbGluZ0NvZGUiLCJpc19hZG1pbiI6ZmFsc2UsImlhdCI6MTczMjg0ODIyOSwiZXhwIjoxNzMzMDIxMDI5fQ.WZReeaxLAWNp3uV_ABiZJwKbBPRpA7fclNBIAwNmMU8'
url = "https://proconvn.duckdns.org"
headers = {"Authorization": PROCON_TOKEN}

def submit(question_id):
    with open(f"sol/sol{question_id}.json", "r", encoding='utf-8') as f:
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