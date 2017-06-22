# coding=utf-8

import easypie.core.game_bindings as game
import easypie.gui.gui_core as gui

gui.init(game.screen)
gui.main_window.centralWidget().editor.file.open('/home/axxessio/workspace/Work/IT4Kids/easypie/examples/MausZumKaese/vorlage.py')
gui.app.exec()
