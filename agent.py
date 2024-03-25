import random
import numpy as np
from collections import deque
import torch
import torch.optim as optim
import torch.nn.functional as F
from model import DQN

class Agent:
    def __init__(self, state_size, action_size, seed=0):
        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(seed)

        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        
        # Replay memory
        self.memory = deque(maxlen=10000)
        self.batch_size = 64

        # Discount factor and exploration rate
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

    def step(self, state, action, reward, next_state, done):
        # Save experience in replay memory
        self.memory.append((state, action, reward, next_state, done))
        
        # Learn every time we have enough samples
        if len(self.memory) > self.batch_size:
            experiences = random.sample(self.memory, self.batch_size)
            self.learn(experiences)

    def act(self, state):
        # Epsilon-greedy action selection
        if random.random() > self.epsilon:
            state = torch.from_numpy(state).float().unsqueeze(0)
            self.model.eval()
            with torch.no_grad():
                action_values = self.model(state)
            self.model.train()
            return np.argmax(action_values.cpu().data.numpy())
        else:
            return random.choice(np.arange(self.action_size))

    def learn(self, experiences):
        states, actions, rewards, next_states, dones = zip(*experiences)
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).view(-1, 1)
        rewards = torch.FloatTensor(rewards).view(-1, 1)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones).view(-1, 1)

        Q_targets_next = self.model(next_states).detach().max(1)[0].unsqueeze(1)
        Q_targets = rewards + (self.gamma * Q_targets_next * (1 - dones))
        Q_expected = self.model(states).gather(1, actions)

        loss = F.mse_loss(Q_expected, Q_targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Update epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon_decay*self.epsilon)

    def save(self, filename):
        torch.save(self.model.state_dict(), filename)

    def load(self, filename):
        self.model.load_state_dict(torch.load(filename))
