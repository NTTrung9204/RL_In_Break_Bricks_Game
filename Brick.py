class Brick:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.isBreak = False

    def set_break(self):
        self.isBreak = True

    def is_broken(self):
        return self.isBreak
    
    def check_collision(self, ball):
        center_ball_x = ball.x
        center_ball_y = ball.y

        radius = ball.radius

        top_brick = self.y
        bottom_brick = self.y - self.height
        left_brick = self.x
        right_brick = self.x + self.width

        closest_x = max(left_brick, min(center_ball_x, right_brick))
        closest_y = max(bottom_brick, min(center_ball_y, top_brick))

        distance = ((center_ball_x - closest_x) ** 2 + (center_ball_y - closest_y) ** 2) ** 0.5

        collision = False
        side = None
        if distance <= radius:
            collision = True
            if center_ball_x > left_brick and center_ball_x < right_brick:
                if center_ball_y >= top_brick:
                    side = "top"
                if center_ball_y <= bottom_brick:
                    side = "bottom"
            if center_ball_y > bottom_brick and center_ball_y < top_brick:
                if center_ball_x <= left_brick:
                    side = "left"
                if center_ball_x >= right_brick:
                    side = "right"

            if center_ball_x < left_brick and center_ball_y > top_brick:
                side = "top_left"

            if center_ball_x > right_brick and center_ball_y > top_brick:
                side = "top_right"

            if center_ball_x < left_brick and center_ball_y < bottom_brick:
                side = "bottom_left"

            if center_ball_x > right_brick and center_ball_y < bottom_brick:
                side = "bottom_right"

        return collision, side
    
    def handle_collision(self):
        self.set_break()

class ManageBrick:
    def __init__(self):
        self.bricks = []
        self.brick_width = 60
        self.brick_height = 30
        self.brick_color = "blue"
        self.brick_space = 10
        self.brick_rows = 2
        self.brick_columns = 10
        self.brick_offset_x = 50
        self.brick_offset_y = 400
        self.create_bricks()

    def create_bricks(self):
        for i in range(self.brick_rows):
            for j in range(self.brick_columns):
                x = self.brick_offset_x + j * (self.brick_width + self.brick_space)
                y = self.brick_offset_y + i * (self.brick_height + self.brick_space)
                self.bricks.append(Brick(x, y, self.brick_width, self.brick_height, self.brick_color))

    def broken_all(self):
        for brick in self.bricks:
            if brick.is_broken() == False:
                return 0
            
        return 1
                