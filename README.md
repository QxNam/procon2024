# Procon 2024

Completed:
- Create board and dies
- Solution


Processing:
- GUI game

## To create a game run:
```bash
python3 gen_data.py
```
Before creating the table, remember to set the initialization parameters.

## To check run:
```bash
python3 solution_simulator.py
```
Before running, remember to name the folder correctly.

```bash
# Example 1:
[[2 3 3 3 1 3]
 [3 3 2 3 3 1]
 [1 2 2 3 3 0]
 [3 0 3 0 0 0]
 [3 2 0 3 2 2]]
> max number of solutions: 1
----------------------------------------
Step 1: 
die: 7, direction: 3, position: (1, 5)
[[2 3 3 3 1 3]
 [3 3 2 3 3 1]
 [1 2 2 3 3 0]
 [3 0 3 0 0 0]
 [3 2 0 3 2 2]]
----------------------------------------
Found solution after 1 steps!
```