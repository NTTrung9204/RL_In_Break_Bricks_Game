from SumTree import SumTree
import random
import numpy as np


class PrioritizedReplayBuffer:
    def __init__(self, capacity, alpha):
        self.tree = SumTree(capacity)
        self.alpha = alpha
        self.epsilon = 0.01
        self.capacity = capacity

    def add(self, error, sample):
        p = (error + self.epsilon) ** self.alpha
        self.tree.add(p, sample)

    def sample(self, n):
        batch = []
        segment = self.tree.total() / n
        priorities = []
        indices = []
        for i in range(n):
            a = segment * i
            b = segment * (i + 1)
            s = random.uniform(a, b)
            idx, p, data = self.tree.get(s)
            priorities.append(p)
            batch.append(data)
            indices.append(idx)
        sampling_probabilities = priorities / self.tree.total()
        is_weights = np.power(self.tree.size * sampling_probabilities, -self.beta())
        return batch, indices, is_weights

    def update(self, idx, error):
        p = (error + self.epsilon) ** self.alpha
        self.tree.update(idx, p)

    def beta(self):
        return 0.4  # For simplicity, we use a constant beta value
    
    def __len__(self):
        return self.capacity
