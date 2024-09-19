from utils import load_json, list_to_matrix
from die_cut import apply_die_cut
from pprint import pprint

# load board and transform to matrix format
question = load_json('question')
game = question['board']['start']
goal = question['board']['goal']
game = list_to_matrix(game)
goal = list_to_matrix(goal)

# load dies and transform to matrix format
dies = load_json('cells')
patterns = {pat['p']: pat['cells'] for pat in question['general']['patterns']}
dies.update(patterns)
dies = {int(p): list_to_matrix(dies[p]) for p in dies}

# # load solve
solve = load_json('answer')
print(solve)

# step1 = solve['ops'][0]
# print(step1)
# die_cut = apply_die_cut(game, dies[str(step1['p'])], step1['x'], step1['y'], step1['s'])

# pprint(die_cut)