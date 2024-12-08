# python .\api\get_test_quest.py --question_id 75
# python .\solution\convert_txt.py --question_id 75       
# g++ -std=c++20 -o solution/solution_z_function.exe solution/solution_z_function.cpp
# solution\solution_z_function.exe 75
# python .\api\post_test_quest.py --question_id 75      

# python main.py --solution z_function --question_id 75


import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--solution", required=True, help="Loại giải pháp (ví dụ: z_function, BFS, BFS_binary_lifting, beam_search)")
parser.add_argument("--question_id", required=True, help="ID câu hỏi")
args = parser.parse_args()

solution_type = args.solution
question_id = args.question_id

subprocess.run(f"python ./api/get_test_quest.py --question_id {question_id}", shell=True, check=True)
subprocess.run(f"python ./solution/convert_txt.py --question_id {question_id}", shell=True, check=True)
subprocess.run(f"g++ -std=c++20 -o solution/solution_{solution_type}.exe solution/solution_{solution_type}.cpp", shell=True, check=True)
subprocess.run(f"solution\solution_{solution_type}.exe {question_id}", shell=True, check=True)
subprocess.run(f"python ./api/post_test_quest.py --question_id {question_id}", shell=True, check=True)