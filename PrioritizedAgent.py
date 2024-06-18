from PrioritizedReplayBuffer import PrioritizedReplayBuffer
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
import numpy as np
import random

class PrioritizedAgent:
    def __init__(self, state_size, action_size, path_model = None):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = PrioritizedReplayBuffer(capacity=50000, alpha=0.6)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9995
        self.learning_rate = 0.001
        if path_model:
            self.model = load_model(path_model)
        else:
            self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim = self.state_size, activation = 'relu'))
        model.add(Dense(64, activation = 'relu'))
        model.add(Dense(128, activation = 'relu'))
        model.add(Dense(self.action_size, activation = 'linear'))
        model.compile(loss = 'mean_squared_error', optimizer = Adam(learning_rate = self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        state = np.reshape(state, [1, self.state_size])
        next_state = np.reshape(next_state, [1, self.state_size])
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0))
        target_f = self.model.predict(state, verbose=0)
        error = abs(target_f[0][action] - target)
        self.memory.add(error, (state, action, reward, next_state, done))

    def get_action(self, state):
        state = np.reshape(state, [1, self.state_size])
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch, indices, is_weights = self.memory.sample(batch_size)
        states = np.array([transition[0] for transition in minibatch]).reshape(batch_size, self.state_size)
        next_states = np.array([transition[3] for transition in minibatch]).reshape(batch_size, self.state_size)
        current_qs = self.model.predict(states, verbose=0)
        next_qs = self.model.predict(next_states, verbose=0)

        loss = 0
        for i, (state, action, reward, next_state, done) in enumerate(minibatch):
            if done:
                target = reward
            else:
                target = reward + self.gamma * np.amax(next_qs[i])
            
            target_f = current_qs[i]
            old_value = target_f[action]
            target_f[action] = target
            
            self.memory.update(indices[i], abs(old_value - target))
            loss += is_weights[i] * (old_value - target) ** 2

        state_X = np.array([transition[0] for transition in minibatch]).reshape(batch_size, self.state_size)
        target_Y = np.array(current_qs)
        
        self.model.fit(state_X, target_Y, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        return loss / batch_size