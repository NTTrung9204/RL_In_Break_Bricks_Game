from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
import numpy as np
import random
import time

class Agent:
    def __init__(self, state_size, action_size, model = None):
        self.state_size = state_size
        self.action_size = action_size

        self.gamma = 0.85
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9995
        self.learning_rate = 0.0005

        self.memory = deque(maxlen=50000)

        if model is None:
            self.model = self._build_model()
            self.epsilon = 1
        else:
            self.model = load_model(model)
            self.epsilon = 0.01

    def _build_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim = self.state_size, activation = 'relu'))
        model.add(Dense(64, activation = 'relu'))
        model.add(Dense(128, activation = 'relu'))
        model.add(Dense(self.action_size, activation = 'linear'))
        model.compile(loss = 'mean_squared_error', optimizer = Adam(learning_rate = self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        action_values = self.model.predict(state, verbose = 0)
        return np.argmax(action_values[0])
    
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        state_X = []
        target_Y = []
        
        # Trích xuất tất cả states và next_states từ minibatch để dự đoán theo batch
        states = np.array([transition[0] for transition in minibatch]).reshape(batch_size, 4)
        next_states = np.array([transition[3] for transition in minibatch]).reshape(batch_size, 4)
        
        # Dự đoán giá trị Q cho tất cả states và next_states trong batch
        current_qs = self.model.predict(states, verbose = 0)
        next_qs = self.model.predict(next_states, verbose = 0)
        
        loss = 0

        for i, (state, action, reward, next_state, done) in enumerate(minibatch):
            if done:
                target = reward
            else:
                target = reward + self.gamma * np.amax(next_qs[i])
            
            target_f = current_qs[i]
            old_value = target_f[action]
            target_f[action] = target
            
            state_X.append(state)
            target_Y.append(target_f)
            
            loss += (old_value - target) ** 2
            
        state_X = np.array(state_X).reshape(batch_size, 4)
        target_Y = np.array(target_Y).reshape(batch_size, 3)

        # Huấn luyện mô hình trên toàn bộ batch
        self.model.fit(state_X, target_Y, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        return loss / batch_size