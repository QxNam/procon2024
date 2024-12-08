---- venv
python3.12 -m venv venv
source venv/bin/activate

---- get question
python3.12 question.py --id {id}

---- solves
python3.12 sol_1_move.py --id {id}

---- post ans
python3.12 submid.py --id {id}
