# coding=utf-8
import pygame

pygame.set_background("./examples/MausZumKaese/background.bmp")


class Kaese(pygame.GameElement):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/home/axxessio/workspace/Work/IT4Kids/easypie/examples/MausZumKaese/Käse.png")
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 1300
        self.rect.y = 60

class Maus(pygame.GameElement):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./examples/MausZumKaese/Maus.bmp")
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 700

sprites = pygame.sprite.Group()
sprites.add(Kaese())
sprites.add()
maus = Maus()
sprites.add(maus)

def game_loop():
    sprites.draw(pygame.screen)

pygame.run(game_loop)