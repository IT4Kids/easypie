# coding=utf-8
import math
import random
import game


class Ball(game.GameElement):
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.width, self.height = self.size = (20, 20)
        # Create the image of the ball
        self.image = game.Surface(self.size)

        # Color the ball
        self.image.fill((255, 255, 255))

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        # Speed in pixels per cycle
        self.speed = 0

        # Floating point representation of where the ball is
        self.x = 0
        self.y = 0

        # Direction of ball in degrees
        self.direction = 0

        # Set the initial ball speed and position
        self.reset()

    def reset(self):
        self.speed = 6.0
        self.x = game.WIDTH / 2
        self.y = game.HEIGHT / 2
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
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        if self.y <= 0 or self.y > game.HEIGHT - self.height:
            self.bounce(0)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y


class Player(game.GameElement):
    # Constructor function
    def __init__(self, x_pos):
        # Call the parent's constructor
        super().__init__()
        self.width = 15
        self.height = 150
        self.image = game.Surface([self.width, self.height])
        self.image.fill((255, 255, 255))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.rect.x = x_pos
        self.rect.y = game.HEIGHT / 2

    # Update the player
    def move(self, distance):
        next_pos = self.rect.y + distance
        if 0 < next_pos < game.HEIGHT-self.height:
            self.rect.y = next_pos


p1_score = 0
p2_score = 0
screen = game.screen
font = game.font.Font(None, 36)
ball = Ball()
p1 = Player(50)
p2 = Player(game.WIDTH - 65)

balls = game.sprite.Group()
balls.add(ball)

moving_sprites = game.sprite.Group()
moving_sprites.add(ball)
moving_sprites.add(p1)
moving_sprites.add(p2)

game.on_key("a", lambda: p1.move(10), method=game.KEYPRESSED)
game.on_key("d", lambda: p1.move(-10), method=game.KEYPRESSED)
game.on_key("j", lambda: p2.move(10), method=game.KEYPRESSED)
game.on_key("l", lambda: p2.move(-10), method=game.KEYPRESSED)


def game_loop():
    global p1_score, p2_score

    screen.fill((0, 0, 0))

    # Print the score
    scoreprint = "Player 1: " + str(p1_score)
    text = font.render(scoreprint, 1, (255, 255, 255))
    textpos = (25, 0)
    screen.blit(text, textpos)

    scoreprint = "Player 2: " + str(p2_score)
    text = font.render(scoreprint, 1, (255, 255, 255))
    textpos = (1450, 0)
    screen.blit(text, textpos)

    if game.sprite.spritecollide(p1, balls, False):
        # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
        diff = 180 + random.randint(-10, 10)  # (p1.rect.x + p1.width / 2) - (ball.rect.x + ball.width / 2)

        # Set the ball's y position in case we hit the ball on the edge of the paddle
        ball.x = 65
        ball.speed += 1
        ball.bounce(diff)

        # See if the ball hits the player paddle
    if game.sprite.spritecollide(p2, balls, False):
        # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
        diff = 180 + random.randint(-10, 10)  # (p2.rect.x + p2.width / 2) - (ball.rect.x + ball.width / 2)

        # Set the ball's y position in case we hit the ball on the edge of the paddle
        ball.x = game.WIDTH - 80
        ball.speed += 1
        ball.bounce(diff)

        # Do we bounce off the vertical side of the screen?
    if ball.x <= p1.rect.x:
        ball.reset()
        p2_score += 1

    if ball.x > p2.rect.x + p2.width:
        ball.reset()
        p1_score += 1

    ball.update()
    p1.update()
    p2.update()

    moving_sprites.draw(screen)

game.run(game_loop)