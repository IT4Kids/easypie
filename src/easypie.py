# coding=utf-8
import gui.gui_core as gui
import core.game_bindings as game

if __name__ == '__main__':
    gui.init(game.screen)
    gui.app.exec()
