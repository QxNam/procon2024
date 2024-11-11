import gym
from gym import spaces
import numpy as np
import pygame
class BoardTransformEnv(gym.Env):
    def __init__(self, board, goal, dies, cell_size=50):
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
        
        # Initialize pygame
        pygame.init()
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
        pygame.display.set_caption("Board Transform Environment")
        self.colors = {
            0: (255, 255, 255),  # White
            1: (0, 0, 255),      # Blue
            2: (0, 255, 0),      # Green
            3: (255, 0, 0)       # Red
        }
    
    def reset(self):
        self.state = self.board.copy()
        self.render()
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
        
        self.render()
        
        return self.state, reward, done, {}
    
    def _apply_die_cutting(self, die, x, y, direction):
        # Implement the die cutting logic here
        # Ví dụ: chỉ là cuộn bảng theo chiều ngang
        self.state = np.roll(self.state, 1, axis=1)
    
    def render(self, mode='human'):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        for i in range(self.height):
            for j in range(self.width):
                color = self.colors.get(self.state[i, j], (0, 0, 0))
                pygame.draw.rect(self.screen, color, 
                                 (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), 
                                 (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size), 1)  # Border
        
        pygame.display.flip()

    def close(self):
        pygame.quit()
    
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