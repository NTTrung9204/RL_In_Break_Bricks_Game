from Brick import Brick, ManageBrick
from Ball import Ball, vector
import random
import math
import numpy as np

class Env:
    def __init__(self):
        self.Width = 800
        self.Height = 600

    def reset(self):
        self.ManagerBrick = ManageBrick()
        self.Shelf = Brick(random.randint(0, self.Height - 200), 50, 200, 20, "blue")
        self.Ball = Ball(10, 200, 10, "red", vector(5, random.uniform(0, 2*math.pi)))
    
    def get_state(self):
        return np.array([self.Shelf.x, self.Ball.x, self.Ball.y, self.Ball.vector.phi])
    
    def step(self, action):
        if action == 0: # Go to left
            self.Shelf.x -= 5
            if self.Shelf.x <= 0:
                self.Shelf.x = 0
        elif action == 1: # Go to right
            self.Shelf.x += 5
            if self.Shelf.x >= self.Width - self.Shelf.width:
                self.Shelf.x = self.Width - self.Shelf.width
        elif action == 2: # freeze
            self.Shelf.x += 0

        self.Ball.move()

        reward = 0

        collision, side = False, None
        for brick in self.ManagerBrick.bricks:
            if brick.is_broken():
                continue
            collision, side = brick.check_collision(self.Ball)
            if collision:
                brick.handle_collision()
                break

        if collision == False:
            collision, side = self.Shelf.check_collision(self.Ball)
            if side in ["top", "top_left", "top_right"]:
                reward += 2

                center_shelf = self.Shelf.x + self.Shelf.width/2
                reward += 0.01 * (100 - abs(self.Ball.x - center_shelf))

        if collision:
            self.Ball.handle_collision(side)

        if self.Ball.x <= self.Ball.radius or self.Ball.x >= self.Width - self.Ball.radius:
            self.Ball.vector.handle_collision("left")

        if self.Ball.y >= self.Height - self.Ball.radius:
            self.Ball.vector.handle_collision("top")

        if self.Ball.y <= self.Ball.radius:
            reward -= 10
            return self.get_state(), reward, True
        
        if self.ManagerBrick.broken_all():
            return self.get_state(), reward, True
        
        return self.get_state(), reward, False
        

