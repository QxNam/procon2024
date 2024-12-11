import argparse
import requests
import json
from config import URL, HEADERS, PWD

# def raw_data():
#     response = requests.get(f"{URL}/question", headers=HEADERS)
#     if response.status_code!= 200:
#         print(f"Failed to get question: {response.status_code}")
#         return None
#     for data in response.json()['data']:
#         _id = data.get('id')
#         with open(f"{PWD}/original_data/{_id}.json", "w", encoding='utf-8') as f:
#             json.dump(data, f, ensure_ascii=False, indent=4)
#         print(f"✅ Saved question id: {_id}")

def process_request(response):
    try:
        id_ = response.get('id')
        question_data = eval(response.get('question_data')) if id_ < 101 else response
        general_die = question_data.get('general', {}).get('patterns',[])
        return {
            "id": id_,
            "h": question_data.get('height'),
            "w": question_data.get('width'),
            "board": question_data.get('start'),
            "goal": question_data.get('goal'),
            "dies": [i.get("cells") for i in general_die]
        }
    except Exception as e:
        print(f"Wrong question {id_}: {e}")
        return None

def get_question(question_id:int=None):
    if question_id:
        response = requests.get(f"{URL}/question/{question_id}", headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to get question {question_id}: {response.status_code}")
            return None
        return process_request(response.json())
    else:
        response = requests.get(f"{URL}/question", headers=HEADERS)
        if response.status_code!= 200:
            print(f"Failed to get question: {response.status_code}")
            return None
        return [process_request(data) for data in response.json()['data']]

# create main function for py 
if __name__ == "__main__":
    #input question_id
    parser = argparse.ArgumentParser(description="Process a question ID.")
    parser.add_argument("--id", type=int, required=False, help="The ID of the question")
    args = parser.parse_args()

    if args.id:
        question_id = args.id
        data = get_question(question_id)
        with open(f"{PWD}/data/{question_id}.json", "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Saved question id: {question_id}")
    else:
        for data in get_question():
            question_id = data['id']
            with open(f"{PWD}/data/{question_id}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ Saved question id: {question_id}")

    # raw_data()
