# coding=utf-8
# coding=utf-8
import random
import pygame

class Ball(pygame.GameElement):
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.width, self.height = self.size = (20, 20)
        self.image = pygame.Surface(self.size)
        self.image.fill((255, 255, 255))
        self.speed = 0
        self.reset()

    def reset(self):

        self.speed = 20.0
        self.x = pygame.WIDTH / 2
        self.y = pygame.HEIGHT / 2
        # Direction of ball (in degrees)
        if random.randint(0,1):
            self.direction = random.randrange(45,135)
        else:
            self.direction = random.randrange(225,315)

    # This function will bounce the ball
    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    # Update the position of the ball
    def update(self):
        self.move(self.speed)
        if self.y <= 0 or self.y > pygame.HEIGHT - self.height:
            self.bounce(0)
        if self.x <= 0 or self.x >= pygame.WIDTH - self.width:
            self.bounce(180)


game_screen = pygame.screen
ball = Ball()

def game_loop():
    ball.update()
    ball.draw(game_screen)

pygame.run(game_loop)
