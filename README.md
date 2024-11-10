# Procon 2024

Get problem and Post answer at `procon_api.ipynb`
First Create `.env` and add `PROCON_TOKEN`

To get problem into json file run `get_problem.py` the json will save in `question_store/{question_id}.json`
```bash
python get_problem.py --question_id {question_id}
```

To plot the question matrix `plot_question.py` add param --question_id, and if --save_image are set `True`, image will save in `question_store/{question_id}.png`
```bash
python plot_question.py --question_id {question_id} --save_image {True/False}
```
