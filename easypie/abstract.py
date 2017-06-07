# coding=utf-8
import pygame


class GameElement(pygame.sprite.Sprite):  # TODO Create game element bindings

    def __init__(self):
        super(GameElement, self).__init__()
        self.x = 300
        pass

    def _move(self):
        import math

        # Change the position (x and y) according to the speed and direction
        direction_radians = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
