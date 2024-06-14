from Agent import Agent
from Env import Env
import sys
import numpy as np

MyEnv = Env()
MyAgent = Agent(4, 3)

batch_size = 256
episodes = 100
max_step = 7000
QuantitiesDone = 0

for episode in range(episodes):
    MyEnv.reset()
    state = MyEnv.get_state()
    state = np.reshape(state, [1, MyAgent.state_size])
    total_reward = 0
    loss = 0
    for step in range(max_step):
        sys.stdout.write(f"\rEpisode {episode}/{episodes}, step {step}, reward {total_reward:.3f}, epsilon {MyAgent.epsilon:.3f}, loss {loss:.3f}")
        action = MyAgent.get_action(state)
        next_state, reward, done = MyEnv.step(action)
        next_state = np.reshape(next_state, [1, MyAgent.state_size])

        MyAgent.remember(state, action, reward, next_state, done)

        state = next_state

        total_reward += reward

        if len(MyAgent.memory) > batch_size:
            loss += MyAgent.replay(batch_size)

        if done:
            if MyEnv.ManagerBrick.broken_all():
                QuantitiesDone += 1
            break

        if np.equal(state[0], MyEnv.get_state()).all() is False:
            print(state[0], MyEnv.get_state())
            raise "State Not Same!"

    if QuantitiesDone < 5 and MyAgent.epsilon <= 0.15:
        MyAgent.epsilon = 0.5
    print()

MyAgent.model.save('Model/DQL_1.keras')

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