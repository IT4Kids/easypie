# coding=utf-8
import pygame

class GameElement(pygame.sprite.Sprite):  # TODO Create game element bindings

    def __init__(self):
        super(GameElement, self).__init__()
        self.x = 300
        pass

    def move(self):
        pass #todo fix gameloop animations with yield

class Animation():#todo create maus zum käse

    def __init__(self):
        self.key_frames = []

    def append(self,kf):
        self.key_frames.append(kf)

    def next(self):
        self.key_frames.pop(0)()
