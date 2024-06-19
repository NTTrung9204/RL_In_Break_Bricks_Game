# Break Brick with Deep Q Learning

This project uses Deep Q Learning to train an agent to play the Break Brick game. The project includes various components to simulate the environment, train the agent, and illustrate the game using Pygame.

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

This project applies Deep Q Learning to develop an agent capable of playing the Break Brick game. The agent is trained to optimize its score by breaking bricks without letting the ball fall.

## Project Structure

The project includes the following files and directories:

- **Agent.py**: Contains the `Agent` class, which includes components such as the model, take_action, replay, and more.
- **Ball.py**: Contains the `Ball` class and the `Vector` class for ball movement.
- **Brick.py**: Contains the `Brick` class and the `ManageBrick` class for handling bricks in the game.
- **Env.py**: Contains classes for the game environment, including rewards and state representation.
- **Main.py**: Illustrates the game using Pygame.
- **PrioritizedAgent.py**: Uses the `Agent` class with prioritized experience replay.
- **PrioritizedReplayBuffer.py**: Class for prioritized replay buffer.
- **SumTree.py**: Class `SumTree` for sampling from the prioritized replay buffer.
- **Training_Agent.py**: Script to train the agent.
- **Model/**: Directory containing pre-trained models.

### Detailed File Descriptions

#### Agent.py
This file defines the `Agent` class, which includes:
- **model**: The neural network model used by the agent.
- **take_action**: A method to decide the next action based on the current state.
- **replay**: A method to perform experience replay and update the model.

#### Ball.py
Defines two classes:
- **Ball**: Represents the ball in the game, handling its movement and collisions.
- **Vector**: A helper class for vector mathematics, used primarily for the ball's movement calculations.

#### Brick.py
Defines two classes:
- **Brick**: Represents a single brick in the game.
- **ManageBrick**: Manages all bricks, including their creation, destruction, and collision detection.

#### Env.py
Contains the environment class for the game, responsible for:
- Defining states, rewards, and game dynamics.
- Providing methods to reset the game and step through actions.

#### Main.py
Illustrates the game using Pygame, showing the agent in action. It visualizes the game state and agent's behavior.

#### PrioritizedAgent.py
Enhances the `Agent` class by implementing prioritized experience replay, which improves learning efficiency by prioritizing important experiences.

#### PrioritizedReplayBuffer.py
Defines a class for prioritized replay buffer, which stores experiences and samples them based on their priority.

#### SumTree.py
Defines the `SumTree` class, which is a data structure used for efficiently sampling from the prioritized replay buffer.

#### Training_Agent.py
Script to train the agent. It initializes the environment, agent, and training loop, saving the model periodically.

#### Model/
Contains pre-trained models that can be used to test the agent without retraining.

## Installation

### Requirements

- Python 3.x
- Pygame
- NumPy
- TensorFlow

### Steps

Clone the repository and install the necessary dependencies:

git clone https://github.com/NTTrung9204/RL_In_Break_Bricks_Game.git
cd RL_In_Break_Bricks_Game
pip install -r requirements.txt

## Usage

### Training the Agent
Run Training_Agent.py to start training the agent:
`python Training_Agent.py`

### Illustrating the Game
After training, you can run Main.py to see the agent playing the game:
`python Main.py`

![image](https://github.com/NTTrung9204/RL_In_Break_Bricks_Game/assets/83105598/57bd97a6-f9e1-4274-b455-52df66feaae3)
