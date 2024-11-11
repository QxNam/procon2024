import gym
from gym import spaces
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class BoardTransformEnv(gym.Env):
    def __init__(self, board, goal, dies):
        super(BoardTransformEnv, self).__init__()
        self.board = board
        self.goal = goal
        self.dies = dies
        self.width, self.height = board.shape
        
        # Define action space: (die_id, x, y, direction)
        self.action_space = spaces.MultiDiscrete([len(dies), self.width, self.height, 4])  # 4 directions
        
        # Define observation space: board state
        self.observation_space = spaces.Box(low=0, high=3, shape=(self.height, self.width), dtype=np.int32)
        self.reset()
        
        # Initialize rendering
        self.fig, self.ax = plt.subplots()
        self.im = None
        self.colors = ['white', 'blue', 'green', 'red']  # Tùy chỉnh màu sắc cho các giá trị
        self.cmap = mcolors.ListedColormap(self.colors)
        self.bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
        self.norm = mcolors.BoundaryNorm(self.bounds, self.cmap.N)
    
    def reset(self):
        self.state = self.board.copy()
        return self.state
    
    def step(self, action):
        # Decode the single integer action into multiple components
        die_id, x, y, direction = self.decode_action(action)
        
        die = self.dies[die_id]
        
        # Apply die cutting operation
        self._apply_die_cutting(die, x, y, direction)
        
        # Calculate reward based on similarity to goal
        reward = -np.sum(self.state != self.goal)  # Negative reward based on differences
        done = np.array_equal(self.state, self.goal)
        
        return self.state, reward, done, {}
    
    def _apply_die_cutting(self, die, x, y, direction):
        # Implement the die cutting logic here
        # Ví dụ: chỉ là cuộn bảng theo chiều ngang
        self.state = np.roll(self.state, 1, axis=1)
    
    def render(self, mode='human'):
        if self.im is None:
            self.im = self.ax.imshow(self.state, cmap=self.cmap, norm=self.norm)
            self.ax.set_title("Board State")
            self.fig.colorbar(self.im, ax=self.ax, ticks=[0, 1, 2, 3], 
                             boundaries=self.bounds)
        else:
            self.im.set_data(self.state)
        
        plt.pause(0.001)  # Cập nhật hình ảnh

    def close(self):
        if self.fig:
            plt.close(self.fig)
            self.fig = None
    
    def encode_action(self, die_id, x, y, direction):
        """Encodes multiple discrete actions into a single integer."""
        return die_id * (self.width * self.height * 4) + x * (self.height * 4) + y * 4 + direction
    
    def decode_action(self, action):
        """Decodes a single integer into multiple discrete actions."""
        direction = action % 4
        action = action // 4
        y = action % self.height
        action = action // self.height
        x = action % self.width
        die_id = action // self.width
        return die_id, x, y, direction