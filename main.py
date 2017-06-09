# coding=utf-8
import easypie.gui.gui_core as gui
import easypie.core.game_bindings as game

RUN_INTEGRATED = True
gui.init(game.screen)
gui.main_window.centralWidget().editor.file.open('./games/pong.py')
gui.app.exec_()
