from Brick import Brick, ManageBrick
from Ball import Ball, vector

from Agent import Agent
from Env import Env

import pygame
import sys
import numpy as np

# ManageBrickInstance = ManageBrick()
# ball = Ball(10, 200, 10, "red", vector(5, 0.3))
# MyEnv.Shelf = Brick(400, 50, 200, 20, "blue")
clock = pygame.time.Clock()

pygame.init()

update = True
MyAgent = Agent(4, 3, "Model/DQL_6.keras")
MyEnv = Env()
total_reward = 0

state = MyEnv.get_state()
state = np.reshape(state, [1, MyAgent.state_size])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Agent make action
    action = MyAgent.get_action(state)
    if action == 0:
        MyEnv.Shelf.x -= 5
    if action == 1:
        MyEnv.Shelf.x += 5

    next_state, reward, done = MyEnv.step(action)
    total_reward += reward
    next_state = np.reshape(next_state, [1, MyAgent.state_size])
    state = next_state
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        MyEnv.Shelf.x -= 5
        if MyEnv.Shelf.x <= 0:
            MyEnv.Shelf.x = 0
        if MyEnv.Shelf.x >= 600:
            MyEnv.Shelf.x = 600
    if keys[pygame.K_RIGHT]:
        MyEnv.Shelf.x += 5

    MyEnv.Ball.move()
    collision = False
    side = None
    for brick in MyEnv.ManagerBrick.bricks:
        if brick.is_broken():
            continue
        collision, side = brick.check_collision(MyEnv.Ball)
        if collision:
            brick.handle_collision()
            update = True
            break

    if collision == False:
        collision, side = MyEnv.Shelf.check_collision(MyEnv.Ball)

    if collision:
        MyEnv.Ball.handle_collision(side)

    if MyEnv.Ball.x <= MyEnv.Ball.radius or MyEnv.Ball.x >= 800 - MyEnv.Ball.radius:
        MyEnv.Ball.vector.handle_collision("left")

    if MyEnv.Ball.y <= MyEnv.Ball.radius or MyEnv.Ball.y >= 600 - MyEnv.Ball.radius:
        MyEnv.Ball.vector.handle_collision("top")

    screen = pygame.display.set_mode((800, 600))
    screen.fill("black")

    if update == True:
        for brick in MyEnv.ManagerBrick.bricks:
            if not brick.is_broken():
                pygame.draw.rect(screen, brick.color, (brick.x, 600 - brick.y, brick.width, brick.height))
        update = True

    if MyEnv.ManagerBrick.broken_all():
        break

    pygame.draw.rect(screen, MyEnv.Shelf.color, (MyEnv.Shelf.x, 600 - MyEnv.Shelf.y, MyEnv.Shelf.width, MyEnv.Shelf.height))

    pygame.draw.circle(screen, MyEnv.Ball.color, (MyEnv.Ball.x, 600 - MyEnv.Ball.y), MyEnv.Ball.radius)

    pygame.display.flip()
    clock.tick(60)

    sys.stdout.write(f"\rReward {total_reward:.3f}, Ball ({MyEnv.Ball.x}, {MyEnv.Ball.y}), Vector ({MyEnv.Ball.vector.x}, {MyEnv.Ball.vector.y})")