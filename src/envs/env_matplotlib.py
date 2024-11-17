import gym
from gym import spaces
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from envs.utils import apply_die_cutting, get_dies

class BoardTransformEnv(gym.Env):
    def __init__(self, board, goal, dies=None):
        super(BoardTransformEnv, self).__init__()
        self.board = board
        self.goal = goal
        self.dies = get_dies()
        if dies:
            self.dies.extend(dies)
        self.width, self.height = board.shape
        
        print('✅ Loaded board:', self.board.shape)
        print('✅ Loaded goal:', self.goal.shape)
        print('✅ Loaded dies:', len(self.dies))

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
        self.die_id = None
        self.x = None
        self.y = None
    
    def reset(self):
        self.die_id = None
        self.x = None
        self.y = None
        self.state = self.board.copy()
        return self.state
    
    def step(self, action):
        # Decode the single integer action into multiple components
        die_id, x, y, direction = self.decode_action(action)
        self.die_id = die_id
        self.x = x
        self.y = y
        
        die = self.dies[die_id]
        
        # Apply die cutting operation
        self.state = apply_die_cutting(self.state, die, x, y, direction)
        
        # Calculate reward based on similarity to goal
        reward = -np.sum(self.state != self.goal)  # Negative reward based on differences
        done = np.array_equal(self.state, self.goal)
        
        return self.state, reward, done, {}
    
    # def render(self, mode='human'):
    #     if self.im is None:
    #         self.im = self.ax.imshow(self.state, cmap=self.cmap, norm=self.norm)
    #         self.ax.set_title("Board State")
    #         self.fig.colorbar(self.im, ax=self.ax, ticks=[0, 1, 2, 3], 
    #                          boundaries=self.bounds)
    #     else:
    #         self.im.set_data(self.state)
    #     # set title for visualization
    #     self.ax.set_title(f"die id: {self.die_id}, ({self.x}, {self.y})")
    #     self.fig.canvas.draw()  # Update the plot
        
    #     plt.pause(0.1)  # Cập nhật hình ảnh

    def render(self, mode='human'):
        if self.im is None:
            # Display the current state
            self.im = self.ax.imshow(self.state, cmap=self.cmap, norm=self.norm)
            # set title for visualization
            self.ax.set_title(f"die id: {self.die_id}, ({self.x}, {self.y})")
            self.fig.canvas.draw()  # Update the plot
            self.fig.colorbar(self.im, ax=self.ax, ticks=[0, 1, 2, 3], 
                            boundaries=self.bounds)
            
            # Create an overlay for mismatched cells
            mismatch = (self.state != self.goal)
            # Use a colormap with a single color for mismatches, e.g., semi-transparent red
            mismatch_cmap = mcolors.ListedColormap(['none', 'red'])
            self.mismatch_overlay = self.ax.imshow(mismatch, cmap=mismatch_cmap, 
                                                alpha=0.5, interpolation='none')
        else:
            # Update the board state
            self.im.set_data(self.state)
            
            # Update the mismatch overlay
            mismatch = (self.state != self.goal)
            self.mismatch_overlay.set_data(mismatch)

        
        
        plt.pause(0.001)  # Update the plot

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
