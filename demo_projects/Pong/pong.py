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

        self.speed = 6.0
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



class Player(pygame.GameElement):
    # Constructor function
    def __init__(self, x_pos):
        # Call the parent's constructor
        super().__init__()
        self.width = 15
        self.height = 150
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))

        self.rect.x = x_pos
        self.rect.y = pygame.HEIGHT / 2

    # Update the player
    def move(self, distance):
        next_pos = self.rect.y + distance
        if 0 < next_pos < pygame.HEIGHT-self.height:
            self.rect.y = next_pos

game_screen = pygame.screen

p1_score = 0
p2_score = 0

ball = Ball()
spieler1 = Player(50)
spieler2 = Player(pygame.WIDTH - 65)

pygame.on_key(pygame.K_a, lambda: spieler1.move(10), method=pygame.KEYPRESSED)
pygame.on_key(pygame.K_d, lambda: spieler1.move(-10), method=pygame.KEYPRESSED)
pygame.on_key(pygame.K_j, lambda: spieler2.move(10), method=pygame.KEYPRESSED)
pygame.on_key(pygame.K_l, lambda: spieler2.move(-10), method=pygame.KEYPRESSED)


def game_loop():
    global p1_score, p2_score


    # Print the score
    pygame.render_text(game_screen, "Player 1: " + str(p1_score), 36, 25, 0)
    pygame.render_text(game_screen, "Player 2: " + str(p2_score), 36, 1400, 0)

    if ball.collides(spieler1):

        # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
        diff = 180 + random.randint(-10, 10)  # (spieler1._rect.x + spieler1.width / 2) - (ball._rect.x + ball.width / 2)
        ball.speed += 1
        ball.bounce(diff)

        # See if the ball hits the player paddle
    if ball.collides(spieler2):
        # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
        diff = 180 + random.randint(-10, 10)  # (spieler2._rect.x + spieler2.width / 2) - (ball._rect.x + ball.width / 2)

        # Set the ball's y position in case we hit the ball on the edge of the paddle
        ball.speed += 1
        ball.bounce(diff)

        # Do we bounce off the vertical side of the game_screen?
    if ball.x <= 0:
        ball.reset()
        p2_score += 1

    if ball.x > pygame.WIDTH:
        ball.reset()
        p1_score += 1

    ball.update()
    spieler1.update()
    spieler2.update()

    ball.draw(game_screen)
    spieler1.draw(game_screen)
    spieler2.draw(game_screen)

pygame.run(game_loop)
