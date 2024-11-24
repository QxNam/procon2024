# train.py
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from envs.env import BoardTransformEnv
from models.dqn import DQN
from replay_buffer import ReplayBuffer, epsilon_greedy_policy

num_episodes = 100  # Tăng số lượng episode để dễ quan sát
gamma = 0.99
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.01
batch_size = 32
learning_rate = 0.001
target_update_frequency = 10

# Initialize environment, model, optimizer, and replay buffer
board = np.array([[2, 2, 0, 1, 0, 3],
                  [2, 1, 3, 0, 3, 3],
                  [0, 2, 2, 1, 0, 3],
                  [3, 2, 2, 0, 3, 3]])

goal = np.array([[0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 2, 2, 2],
                 [2, 2, 2, 2, 3, 3],
                 [3, 3, 3, 3, 3, 3]])

dies = [np.array([[1, 0], [0, 1]]), np.array([[1, 1], [1, 0]])]  # Example dies
env = BoardTransformEnv(board, goal, dies)

action_size = np.prod(env.action_space.nvec)
model = DQN(board.size, action_size)
target_model = DQN(board.size, action_size)
target_model.load_state_dict(model.state_dict())
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
replay_buffer = ReplayBuffer(10000)

# Training loop
for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    
    for t in range(100):  # Limit steps per episode
        action = epsilon_greedy_policy(state, epsilon, model, env.action_space, env)
        next_state, reward, done, _ = env.step(action)
        replay_buffer.push((state, action, reward, next_state, done))
        
        total_reward += reward
        state = next_state
        
        if replay_buffer.size() >= batch_size:
            # Sample a batch from replay buffer
            batch = replay_buffer.sample(batch_size)
            states, actions, rewards, next_states, dones = zip(*batch)
            
            # Convert lists of numpy arrays to single numpy arrays
            states = np.array([np.array(s) for s in states])
            actions = np.array(actions)
            next_states = np.array([np.array(s) for s in next_states])
            
            # Convert to tensors
            states = torch.FloatTensor(states)
            actions = torch.LongTensor(actions)
            rewards = torch.FloatTensor(rewards)
            next_states = torch.FloatTensor(next_states)
            dones = torch.FloatTensor(dones)
    
            # Flatten the states if necessary
            states = states.view(states.size(0), -1)  # [batch_size, board_size]
            next_states = next_states.view(next_states.size(0), -1)
    
            # Compute Q-values for the actions taken
            q_values = model(states).gather(1, actions.view(-1, 1))  # [batch_size, 1]
            q_values = q_values.squeeze(1)  # [batch_size]
    
            # Compute the target Q-values (from target model)
            next_q_values = target_model(next_states).max(1)[0]  # [batch_size]
            targets = rewards + gamma * next_q_values * (1 - dones)  # [batch_size]
    
            # Compute loss and update model
            loss = nn.MSELoss()(q_values, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        if done:
            break
    
    # Update epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)
    
    # Update target model
    if (episode + 1) % target_update_frequency == 0:
        target_model.load_state_dict(model.state_dict())
    
    print(f"Episode {episode+1}/{num_episodes}, Total Reward: {total_reward}")

env.close()  # Đóng cửa sổ khi kết thúc
