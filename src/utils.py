import torch
import random
import imageio.v2 as imageio
import numpy as np
import matplotlib.pyplot as plt

def update_target_network(policy_net, target_net):
    target_net.load_state_dict(policy_net.state_dict())

def select_action(state, policy_net, epsilon, n_actions):
    if random.random() < epsilon:
        return random.randint(0, n_actions - 1)
    else:
        state = torch.FloatTensor(state).unsqueeze(0).unsqueeze(0)
        with torch.no_grad():
            q_values = policy_net(state)
        return q_values.max(1)[1].item()

def plot_board(state, goal, episode, step):
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(state, cmap='viridis', vmin=0, vmax=3)
    plt.title(f"Current State (Episode {episode}, Step {step})")
    plt.colorbar()

    plt.subplot(1, 2, 2)
    plt.imshow(goal, cmap='viridis', vmin=0, vmax=3)
    plt.title("Goal State")
    plt.colorbar()
    plt.show()

def save_frame_to_video(writer, state, goal, episode, step):
    fig, axes = plt.subplots(1, 2, figsize=(4, 2))
    im1 = axes[0].imshow(state, cmap='viridis', vmin=0, vmax=3)
    axes[0].set_title(f"Ep {episode}, Step {step}")
    fig.colorbar(im1, ax=axes[0])

    im2 = axes[1].imshow(goal, cmap='viridis', vmin=0, vmax=3)
    axes[1].set_title("Goal")
    fig.colorbar(im2, ax=axes[1])

    plt.tight_layout()
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    writer.append_data(image)
    plt.close(fig)
