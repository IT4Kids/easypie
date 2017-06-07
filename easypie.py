# coding=utf-8
import gui.core
import game

RUN_INTEGRATED = True

game.init()
gui.core.init(game.screen)
gui.core.main_window.centralWidget().editor.file.open('./games/pong.py')
gui.core.app.exec_()
