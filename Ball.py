import math
import random

class Ball:
    def __init__(self, x, y, radius, color, vector):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vector = vector

    def move(self):
        self.x += self.vector.x
        self.y += self.vector.y

    def handle_collision(self, side):
        self.vector.handle_collision(side)


class vector:
    def __init__(self, a, phi):
        self.a = a
        self.phi = phi
        self.update()

    def standardized_angle_phi(self):
        # make sure angle phi in range(0, 2PI)
        if self.phi < 0:
            self.phi += 2 * math.pi
        
        if self.phi > 2 * math.pi:
            self.phi -= 2 * math.pi

    def handle_collision_vertical(self):
        self.phi = -self.phi
        self.standardized_angle_phi()
    
    def handle_collision_horizontal(self):
        self.phi = math.pi - self.phi
        self.standardized_angle_phi()

    def handle_collision_corner(self):
        self.phi = math.pi + self.phi
        self.standardized_angle_phi()

    def update(self):
        if random.random() <= 0.05:
            self.phi += random.uniform(-0.1, 0.1)
        self.standardized_angle_phi()
        self.x = self.a * math.cos(self.phi)
        self.y = self.a * math.sin(self.phi)

    def handle_collision(self, side):
        if side == "top" or side == "bottom":
            self.handle_collision_vertical()
        if side == "left" or side == "right":
            self.handle_collision_horizontal()
        if side == "top_left" or side == "top_right" or side == "bottom_left" or side == "bottom_right":
            self.handle_collision_corner()
        self.update()


        
        