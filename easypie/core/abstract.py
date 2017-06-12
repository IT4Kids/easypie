# coding=utf-8
import pygame

class GameElement(pygame.sprite.Sprite):

    def __init__(self):
        super(GameElement, self).__init__()
        self.costume = None


class Animation():

    def __init__(self):
        self.key_frames = []

    def append(self,kf):
        self.key_frames.append(kf)

    def next(self):
        self.key_frames.pop(0)()
