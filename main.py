# coding=utf-8
import pygame

import easypie.gui.gui_core as gui
import easypie.core.game_bindings as game

pygame.init()
gui.init(game.screen)
gui.main_window.centralWidget().editor.file.open('/home/axxessio/workspace/Work/IT4Kids/easypie/examples/MausZumKaese/vorlage.py')
ret = gui.app.exec_()
pygame.quit()
