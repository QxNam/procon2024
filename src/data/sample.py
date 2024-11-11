import json
from pprint import pprint

def get_questions(path:str) -> dict:
    with open(path, 'r') as f:
        response = json.load(f)
    return {
        'response': response,
        'data': json.loads(response.get('question_data'))
    }

if __name__ == '__main__':
    data = get_questions('66.json')
    pprint(data['data'].keys())