from utils import apply_die_cutting, load_data, save_figure, create_json_submit
import numpy as np
import sys
from time import time
import argparse

class Point():
    def __init__(self, x: int, y: int, p:int=None, s:int=None, par=None):
        self.x = x
        self.y = y
        self.p = p
        self.s = s
        self.par = par

class Solve():
    def __init__(self, id, h, w, board, goal, dies):
        self.id = id
        self.x = 0
        self.y = 0
        self.h = h
        self.w = w
        self.board = board
        self.state = board
        self.goal = goal
        self.dies = dies
        self.root = None
        self.index_dies = [0, 1, 4, 7, 10, 13, 16, 19, 22]
        self.unique = set()
    
    def next_column(self):
        self.y = 0
        self.x += 1
    
    def get_action(self, x=0, y=0, x_min=0, y_min=0) -> dict:
        direct_2 = []

        for i in range(int(np.log2(self.w))):
            if x + 2**i < w:
                direct_2.append((x + 2**i, y))
        
        direct_0 = []
        direct_1 = []
        for i in range(int(np.log2(self.h))):
            if y + 2**i < h:
                direct_0.append((x, y + 2**i))
            if y - 2**i >= 0 and x != x_min:
                direct_1.append((x, y - 2**i))
        
        return {
            1: direct_1,
            0: direct_0,
            2: direct_2,
        }

    def backtrack(self, node: Point) -> list:
        result = []
        while node.par:
            p, s, x, y = node.p, node.s, node.x, node.y+1
            node = node.par
            if s != 1:
                x, y = node.x, node.y

            result.append({
                'p': p,
                'x': x,
                'y': y,
                's': s
            })
        return result
    
    def bfs(self) -> dict:
        x_min, y_min = self.x, self.y
        target = self.goal[self.y][self.x]
        visited = set()
        self.root = Point(self.x, self.y)
        queue = [self.root]

        while queue:
            node = queue.pop(0)
            visited.add((node.x, node.y))
            if self.state[node.y][node.x] == target:
                return self.backtrack(node)
            
            actions = self.get_action(node.x, node.y, x_min, y_min)
            for s, points in actions.items():
                for p, (x, y) in enumerate(points):
                    if (x, y) in visited:
                        continue
                    new_node = Point(x, y, self.index_dies[p], s)
                    new_node.par = node
                    queue.append(new_node)

    def search(self, n_step=None):
        all_results = []
        n = 0
        s = time()
        while not np.all(self.state == self.goal):
            if self.y == self.h:
                self.next_column()
            if self.state[self.y][self.x] == self.goal[self.y][self.x]:
                self.y += 1
                continue
            results = self.bfs()
            for res in results:
                self.state = apply_die_cutting(self.state, self.dies[res['p']], res['x'], res['y'], res['s'])
            all_results.extend(results)

            # Cập nhật thông tin hiển thị
            progress_info = f"Step: {n+1}, {sum((self.state==self.goal).astype(int).flatten())}/{self.h*self.w}"
            print('\r' + progress_info, end='')
            sys.stdout.flush()  # Đảm bảo thông tin được in ngay lập tức

            self.y += 1
            n+=1
            if n_step and n >= n_step:
                break

        # save_figure(id=self.id, state=self.state, goal=self.goal)
        create_json_submit(self.id, all_results)
        print(f'\nCount of results: {len(all_results)}, Time: {time()-s:.2f}s')

    def next_points(self, x=0, y=0) -> list:
        points = []
        new_point = [(x+1, y), (x, y+1)]
        for p in new_point:
            if p[0] < self.w and p[1] < self.h and p not in self.unique:
                points.append(p)
        return points
    
    def search_2(self, n_step=None):
        all_results = []
        n = 0
        queue = [(0, 0)]
        while not np.all(self.state == self.goal):
            # if self.y == self.h:
            #     self.next_column()
            x, y = queue.pop(0)
            self.unique.add((x, y))
            points = self.next_points(x, y)
            for p in points:
                self.unique.add(p)
            queue.extend(points)
            self.x = x
            self.y = y
            if self.state[self.y][self.x] == self.goal[self.y][self.x]:
                continue
            results = self.bfs()
            for res in results:
                self.state = apply_die_cutting(self.state, self.dies[res['p']], res['x'], res['y'], res['s'])
            all_results.extend(results)
            
            n+=1
            if n_step and n >= n_step:
                break
        
        # save_figure(self.id, self.state, self.goal)
        create_json_submit(self.id, all_results)
        print(f'Count of results: {len(all_results)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Submit a solution.")
    parser.add_argument("--id", type=int, required=True, help="The ID of the question")
    args = parser.parse_args()
    _id = args.id
    data = load_data(_id)
    board = data['board'].copy()
    goal = data['goal'].copy()
    dies = data['dies']
    w = data['w']
    h = data['h']

    solve = Solve(_id, h, w, board, goal, dies)
    solve.search()