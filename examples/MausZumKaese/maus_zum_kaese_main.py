# coding=utf-8
import math
import functools
import time

import pygame




class Kaese(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Käse.png")
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 1300
        self.rect.y = 60


def chunkify(value,chunksize=10):
    abs_value = abs(value)
    sign = value/abs_value
    chunks = []
    while abs_value != 0:
        if abs(abs_value - chunksize) >= 0:
            chunks.append(chunksize*sign)
            abs_value -= 10
        else:
            chunks.append(abs_value*sign)
            break
    return chunks


class Maus(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

    def move(self,steps=10):
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.rect.x += steps * math.sin(direction_radians)
        self.rect.y += steps * math.cos(direction_radians)

    def turn(self, rad=15):
        self.direction += rad
        loc = self.rect.center
        self.image = pygame.transform.rotate(self.original_image,self.direction-90)
        self.rect = self.image.get_rect(center=loc)

    def reset(self):
        self.original_image = pygame.transform.scale2x(pygame.image.load("Maus.bmp"))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 50,700
        self.direction = 90
maus = Maus()


class Animation:
    def __init__(self):
        self.key_frames = []
        self.waittime = 1
        self.last_time = 0

    def add(self, func, *args, wait_time=0.01, **kwargs):
        if args and func in [maus.move,maus.turn]:
            for steps in chunkify(args[0]):
                self.key_frames.append((functools.partial(func, steps, **kwargs), wait_time))

        else:
            self.key_frames.append((functools.partial(func, *args, **kwargs), wait_time))
            return


    def update(self):
        if not self.last_time:
            self.last_time = time.time()
        # We can't use time.time() in a variable since the animation call can take a long time.
        if time.time() > self.last_time + self.waittime:
            if self.key_frames:
                func_tuple = self.key_frames.pop(0)
                func_tuple[0]()
                self.waittime = func_tuple[1]
            self.last_time = time.time()

class WaterCollider(pygame.sprite.Sprite):

    def __init__(self,x,y,width,height,groups):
        super().__init__(groups)
        self.image = pygame.Surface((width,height))
        self.image.fill((0,0,255))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

watercolliders = pygame.sprite.Group()
WaterCollider(0,0,100,500,watercolliders)
WaterCollider(0,0,1000,80,watercolliders)
WaterCollider(620,370,1000,600,watercolliders)
maus_group = pygame.sprite.Group()
maus_group.add(maus)

k = Kaese()
kaese_group = pygame.sprite.Group()
kaese_group.add(k)

font = pygame.font.Font(None, 220)
def game_loop(anim):
    global won,lost
    if not won and not lost:
        anim.update()
        maus_group.draw(pygame.screen)
        kaese_group.draw(pygame.screen)
        watercolliders.draw(pygame.screen)
        if pygame.sprite.spritecollide(maus, watercolliders, False):
            lost = True
        if pygame.sprite.spritecollide(maus,kaese_group, False):
            won = True

    if won:
        maus.rect.x = pygame.WIDTH / 2 - maus.rect.width/2
        maus.rect.y = pygame.HEIGHT / 2 - 200
        text = font.render("Gewonnen!", True, (255, 255, 255))
        pygame.screen.blit(text, (200, 400))
        maus_group.draw(pygame.screen)
        pygame.set_background()


    if lost:
        maus.rect.x = pygame.WIDTH / 2 - maus.rect.width/2
        maus.rect.y = pygame.HEIGHT / 2 - 200
        text = font.render("Verloren!", True, (255, 0, 0))
        pygame.screen.blit(text, (250, 400))
        maus_group.draw(pygame.screen)
        pygame.set_background()

def run(anim):
    global  won,lost
    pygame.set_background("background.bmp")
    maus.reset()
    won, lost = False, False
    pygame.run(lambda: game_loop(anim))
