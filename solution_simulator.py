from procon.utils import load_json, list_to_matrix, check_goal
from procon.die_cut import apply_die_cut
from pprint import pprint


def simulator():
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

    # # # load solve
    solve = load_json('answer')
    print(game)
    print(f'> max number of solutions: {solve["n"]}')
    print('--'*20)
    for idx, step in enumerate(solve['ops'], 1):
        print(f'Step {idx}: ')
        print(f'die: {step["p"]}, direction: {step["s"]}, position: ({step["x"]}, {step["y"]})')
        game = apply_die_cut(game, dies[step['p']], step['x'], step['y'], step['s'])
        print(game)
        print('--'*20)
        if check_goal(game, goal):
            print(f'Found solution after {len(solve["ops"])} steps!')
            break
        if idx == solve['n']:
            print(f'No solution found after {len(solve["ops"])} steps!')


if __name__ == "__main__":
    simulator()