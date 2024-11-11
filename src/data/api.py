import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('.env')
PROCON_TOKEN = os.environ.get('PROCON_TOKEN')

url = "https://proconvn.duckdns.org"
headers = {"Authorization": PROCON_TOKEN}

def get_questions(question_id:int=66) -> dict:
    response = requests.get(f"{url}/question/{question_id}", headers=headers).json()
    if response.status_code != 200:
            return None
    return {
        'response': response,
        'data': json.loads(response.get('question_data'))
    }