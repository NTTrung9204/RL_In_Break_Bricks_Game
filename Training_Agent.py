from Agent import Agent
from PrioritizedAgent import PrioritizedAgent
from Env import Env
import sys
import numpy as np
import math

MyEnv = Env()
MyAgent = PrioritizedAgent(4, 3, "Model/DQL_6.keras")

batch_size = 256
episodes = 29
max_step = 7000
QuantitiesDone = 0

for episode in range(episodes):
    MyEnv.reset()
    state = MyEnv.get_state()
    state = np.reshape(state, [1, MyAgent.state_size])
    total_reward = 0
    loss = 0
    for step in range(max_step):
        if step % 2 == 0 or (state[0][-1] >= math.pi and state[0][-1] <= 2 * math.pi and state[0][-2] <= 300):
            action = MyAgent.get_action(state)
        else:
            action = 2 # do nothing
        sys.stdout.write(f"\rEpisode {episode}/{episodes}, step {step}, reward {total_reward:.3f}, epsilon {MyAgent.epsilon:.3f}, loss {loss:.3f}, action {action}")
        next_state, reward, done = MyEnv.step(action)
        next_state = np.reshape(next_state, [1, MyAgent.state_size])

        if step % 2 == 0 or (state[0][-1] >= math.pi and state[0][-1] <= 2 * math.pi and state[0][-2] <= 300):
            # state[0][-1]: angle phi of vector, capture when ball drop
            # state[0][-2]: coordinate y of ball
            MyAgent.remember(state, action, reward, next_state, done)

        state = next_state

        total_reward += reward

        if total_reward >= 100:
            break

        if MyAgent.memory.tree.size > batch_size:
            loss += MyAgent.replay(batch_size)

        if done:
            if MyEnv.ManagerBrick.broken_all():
                print(f" Win Game! Total Reward {total_reward:.3f}")
                QuantitiesDone += 1
            else:
                print(f" Total Reward {total_reward:.3f}")
            break

        if np.equal(state[0], MyEnv.get_state()).all() is False:
            print(state[0], MyEnv.get_state())
            raise "State Not Same!"

    if QuantitiesDone < 10 and MyAgent.epsilon <= 0.1:
        MyAgent.epsilon = 0.5

    if (episode + 1) % 10 == 0:
        MyAgent.model.save(f'Model/DQL_7.{episode}.keras')

MyAgent.model.save('Model/DQL_7.keras')

MyAgent.epsilon = 0.01
MyEnv.reset()
state = MyEnv.get_state()
state = np.reshape(state, [1, MyAgent.state_size])
total_reward = 0
for step in range(max_step):
    action = MyAgent.get_action(state)
    next_state, reward, done = MyEnv.step(action)
    next_state = np.reshape(next_state, [1, MyAgent.state_size])
    state = next_state
    total_reward += reward
    if np.equal(state[0], MyEnv.get_state()).all() is False:
        print(state[0], MyEnv.get_state())
        raise "State Not Same!"
    if done:
        break

print(f"Total Reward: {total_reward}")
print(MyEnv.ManagerBrick.broken_all())