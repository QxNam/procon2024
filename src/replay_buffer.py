from collections import deque
import random
import torch

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, experience):
        self.buffer.append(experience)
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def size(self):
        return len(self.buffer)

def epsilon_greedy_policy(state, epsilon, model, action_space, env):
    if random.random() < epsilon:
        action_components = action_space.sample()  # Random action as MultiDiscrete
        action = env.encode_action(*action_components)  # Encode to single integer
        return action
    else:
        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0)
            q_values = model(state)
            return q_values.argmax().item()  # Choose action with max Q-value

