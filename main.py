from fastapi import FastAPI, HTTPException
import json
import glob
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load all JSON files from the folder and store them in a dictionary
data_dict = {}

for file_path in glob.glob('test_problem/*.json'):
    with open(file_path, 'r') as f:
        data = json.load(f)
        data_id = data.get("id")
        if data_id is not None:
            data_dict[data_id] = data


@app.get("/")
def healcheck():
    return {"status": "ok"}


@app.get("/data_info")
def data_info():
    if data_dict:
        return {"status": "ok", "number_of_data": len(data_dict), "start_index": min(data_dict.keys()), "end_index": max(data_dict.keys())}
    else:
        return {"status": "error when load data"}


@app.post("/submit_answer")
def submit_answer(data_ans: dict):
    user_id = data_ans.get('user_id')
    question_id = data_ans.get('question_id')
    if question_id is None:
        raise HTTPException(status_code=400, detail="question_id is required in data_ans")

    # Create the submit directory if it doesn't exist
    try:
        os.makedirs('submit', exist_ok=True)
        # Define the file path
        file_path = f'./submit/{user_id}_{question_id}.json'
        # Save the solve data to the file
        with open(file_path, 'w') as f:
            json.dump(data_ans, f)

        return {"status": "success", "file_path": file_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/get_data/")
def get_data(id: int):
    # Find the data with the given id
    if id in data_dict:
        return data_dict[id]
    raise HTTPException(status_code=404, detail="Item not found")


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True)
