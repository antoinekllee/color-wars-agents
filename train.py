from game_env import GameEnv
from agent import Agent
import numpy as np

episodes = 1000  # Total episodes to run
state_size = 5 * 5 * 2  # A 5x5 grid with 2 channels (one for each player)
action_size = 25  # Each cell in the 5x5 grid can be an action

def train(episodes):
    env = GameEnv()  # Initialize the game environment
    agent = Agent(state_size, action_size)  # Initialize the RL agent
    
    for episode in range(1, episodes + 1):
        state = env.reset()  # Reset the environment for a new episode
        state = np.reshape(state, [1, state_size])  # Flatten the state for the DQN
        done = False
        total_reward = 0

        while not done:
            action = agent.act(state)  # Agent chooses an action
            next_state, reward, done, _ = env.step(action)  # Environment responds
            next_state = np.reshape(next_state, [1, state_size])
            
            agent.step(state, action, reward, next_state, done)  # Agent learns
            
            state = next_state
            total_reward += reward

            if done:
                print(f"Episode: {episode}, Total reward: {total_reward}, Epsilon: {agent.epsilon:.2}")
                break
        
        # Save the model every 50 episodes
        if episode % 50 == 0:
            agent.save(f"model_{episode}.pth")

if __name__ == "__main__":
    train(episodes)
