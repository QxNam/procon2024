# Procon 2024

Completed:
- Create board and dies
- Solution


Processing:
- GUI game

## Run simulation with initialization in data
```bash
python3 solution_simulator.py
```

```Output
[[2 2 0 1 0 3]
 [2 1 3 0 3 3]
 [0 2 2 1 0 3]
 [3 2 2 0 3 3]]
> max number of solutions: 3
----------------------------------------
Step 1: 
die: 4, direction: 2, position: (1, 1)
[[1 1 1 1]
 [1 1 1 1]
 [1 1 1 1]
 [1 1 1 1]]
[[2 2 0 1 0 3]
 [1 3 0 3 2 3]
 [2 2 1 0 0 3]
 [2 2 0 3 3 3]]
----------------------------------------
Step 2: 
die: 11, direction: 3, position: (3, -12)
[[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]]
[[2 2 0 1 0 3]
 [1 3 0 3 2 3]
 [2 2 1 0 0 3]
 [2 2 0 3 3 3]]
----------------------------------------
Step 3: 
die: 25, direction: 0, position: (3, 3)
[[0 1 1 1]
 [1 0 0 1]]
[[2 2 0 1 3 3]
 [1 3 0 3 0 3]
 [2 2 1 0 2 3]
 [2 2 0 3 0 3]]
----------------------------------------
No solution found after 3 steps!
```