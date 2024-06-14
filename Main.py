from Brick import Brick, ManageBrick
from Ball import Ball, vector

import pygame
import sys

ManageBrickInstance = ManageBrick()
ball = Ball(10, 200, 10, "red", vector(5, 0.3))
shelf = Brick(400, 50, 200, 20, "blue")
clock = pygame.time.Clock()

pygame.init()

update = True

step = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        shelf.x -= 5
        if shelf.x <= 0:
            shelf.x = 0
        if shelf.x >= 600:
            shelf.x = 600
    if keys[pygame.K_RIGHT]:
        shelf.x += 5

    ball.move()
    collision = False
    side = None
    for brick in ManageBrickInstance.bricks:
        if brick.is_broken():
            continue
        collision, side = brick.check_collision(ball)
        if collision:
            brick.handle_collision()
            update = True
            break

    if collision == False:
        collision, side = shelf.check_collision(ball)

    if collision:
        ball.handle_collision(side)

    if ball.x <= ball.radius or ball.x >= 800 - ball.radius:
        ball.vector.handle_collision("left")

    if ball.y <= ball.radius or ball.y >= 600 - ball.radius:
        ball.vector.handle_collision("top")

    screen = pygame.display.set_mode((800, 600))
    screen.fill("black")

    if update == True:
        for brick in ManageBrickInstance.bricks:
            if not brick.is_broken():
                pygame.draw.rect(screen, brick.color, (brick.x, 600 - brick.y, brick.width, brick.height))
        update = True

    if ManageBrickInstance.broken_all():
        break

    pygame.draw.rect(screen, shelf.color, (shelf.x, 600 - shelf.y, shelf.width, shelf.height))

    pygame.draw.circle(screen, ball.color, (ball.x, 600 - ball.y), ball.radius)

    pygame.display.flip()
    clock.tick(60)

    step += 1
    print(step)