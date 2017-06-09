# coding=utf-8
import gui.gui_core
import easypie.user_bindings as game

RUN_INTEGRATED = True
gui.gui_core.init(game.screen)
gui.gui_core.main_window.centralWidget().editor.file.open('./games/pong.py')
gui.gui_core.app.exec_()
