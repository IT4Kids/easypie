# coding=utf-8
import src.gui.gui_core as gui
import src.core.game_bindings as game
import examples.MausZumKaese.maus_zum_kaese_main #TODO Restructure, temporary fix for missing files in dist version

if __name__ == '__main__':
    gui.init(game.screen)
    gui.app.exec()
