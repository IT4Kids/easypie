# coding=utf-8
import easypie.gui.gui_core as gui
import easypie.core.game_bindings as game
import examples.MausZumKaese.maus_zum_kaese_main #TODO Restructure, temporary fix for missing files in dist version

gui.init(game.screen)
gui.main_window.centralWidget().editor.file.open('/home/axxessio/workspace/Work/IT4Kids/easypie/examples/MausZumKaese/vorlage.py')
gui.app.exec()
