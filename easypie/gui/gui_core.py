# coding=utf-8
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import pygame
from PyQt5.QtCore import Qt

import easypie.signals
import easypie.gui.editor
import easypie.gui.debug_console
import easypie.core.game_bindings as bindings
import easypie.core.constants as constants
main_window = None
app = None

def get_window():
    return main_window

class QCanvas(QtWidgets.QFrame):
    def __init__(self, pygame_surface, parent=None):
        super(QCanvas, self).__init__(parent)

        self.buffer = pygame_surface
        self.screen = self.buffer
        self.border_size = 5
        self.w, self.h = 100-self.border_size, 100-self.border_size
        self.painter = QtGui.QPainter()
        self.setMinimumSize(self.w, self.h)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.painting_enabled = False
        self.backdrop_image = None

        easypie.signals.all.game_start_signal.connect(self.play)
        easypie.signals.all.game_stop_signal.connect(self.stop)

        self.toggle_fs_action = QtWidgets.QAction("Fullscreen")
        self.toggle_fs_action.triggered.connect(self.toggle_fullscreen)
        self.toggle_fs_action.setShortcut("f10")
        self.addAction(self.toggle_fs_action)

        self.exit_focus_action = QtWidgets.QAction("Exit Focus")
        self.exit_focus_action.triggered.connect(lambda: self.toggle_fullscreen(True))
        self.exit_focus_action.setShortcut("esc")
        self.addAction(self.exit_focus_action)

    def toggle_fullscreen(self,state=None):
        state = state if state else self.isWindow()
        if state:
            self.setWindowFlags(self.windowFlags() & ~Qt.Window)
            self.setFocus()
            self.show()
        else:
            self.setWindowFlags(Qt.Window)
            self.showFullScreen()

    def play(self,code):
        self.painting_enabled = True
        self.setStyleSheet("background-color: rgb(0,0,0); border: 5px solid #38b259;")

    def closeEvent(self, event):
        self.toggle_fullscreen()
        event.ignore()

    def stop(self):
        self.setStyleSheet("background-color: rgb(0,0,0); border: 5px solid #c43c27;")
        self.buffer.fill((0,0,0))
        self.painting_enabled = False

    def qt_to_sdl_press(self, key_code):
        return key_code+32

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        modifiers = int(QtGui.QGuiApplication.keyboardModifiers())
        print("KeyPressEvent:", event.key(), event.text())
        key = self.qt_to_sdl_press(event.key())
        if event.isAutoRepeat():
            if key not in bindings.pressed_keys:
                bindings.pressed_keys.append(key)
        else:
            method = constants.KEYDOWN
            bindings.key_queue.append((method, key, modifiers))
            bindings.pressed_keys.append(key)

    def keyReleaseEvent(self, event):
            if self.qt_to_sdl_press(event.key()) in bindings.pressed_keys:
                bindings.pressed_keys.remove(self.qt_to_sdl_press(event.key()))

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.setCursor(QtCore.Qt.BlankCursor)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def paintEvent(self, event):
        if self.painting_enabled:
            self.painter.begin(self)
            scaled_buffer = pygame.transform.scale(self.buffer.copy(), (self.w, self.h))
            image = QtGui.QImage(scaled_buffer.get_buffer().raw, self.w, self.h, QtGui.QImage.Format_RGB32)
            self.painter.drawImage(self.border_size, self.border_size, image)
            self.painter.end()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.w, self.h = self.width()-self.border_size*2, self.height()-self.border_size*2


class QStage(QtWidgets.QWidget):
    def __init__(self, pygame_canvas, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setSpacing(5)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.canvas = QCanvas(pygame_canvas)
        self.layout().addWidget(self.canvas, 50)

        self.console = easypie.gui.debug_console.QDbgConsole((100, 100))
        self.layout().addWidget(self.console, 50)

    def play(self, code):
        self.console.clear()
        self.console.write("Starting program.")
        self.canvas.play()
        bindings._execute(code)

    def stop(self):
        bindings._game_thread.stop()
        self.canvas.stop()

    def pause(self):
        bindings._game_thread.paused = not bindings._game_thread.paused


class MainWidget(QtWidgets.QWidget):
    def __init__(self, pygame_canvas, parent=None):
        super(MainWidget, self).__init__(parent)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.stage = QStage(pygame_canvas)
        self.editor = easypie.gui.editor.Editor()

        self.layout().addWidget(self.stage, 50)
        self.layout().addWidget(self.editor, 50)

class PlaceHolderWidget(QtWidgets.QTextEdit):
    def __init__(self, size=None, parent=None):
        super().__init__(parent)
        if size:
            self.setMinimumSize(*size)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, pygame_canvas, parent=None):
        super(MainWindow, self).__init__(parent)
        #General Setup
        self.setCentralWidget(MainWidget(pygame_canvas))
        self.setMinimumSize(1024, 768)
        self.setWindowIcon(QtGui.QIcon("./easypie/gui/res/icon.png"))
        self.setWindowTitle("It4Kids: EasyPie")
        self.setStyleSheet(open("./easypie/gui/style.css").read()) #Todo make configurable

        #Setup Toolbar
        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(40, 40))

        play_action = toolbar.addAction(QtGui.QIcon('./easypie/gui/res/play.png'),
                                        "Play (F5)",
                                        lambda: easypie.signals.all.game_start_signal.emit(
                                            self.centralWidget().editor.toPlainText()))
        play_action.setShortcut("f5")
        play_action.setShortcutContext(Qt.ApplicationShortcut)

        stop_action = toolbar.addAction(QtGui.QIcon('./easypie/gui/res/stop.png'),
                                        "Stop (F6)",
                                        lambda: easypie.signals.all.game_stop_signal.emit())
        stop_action.setShortcut("f6")
        stop_action.setShortcutContext(Qt.ApplicationShortcut)

        self.toolBar = toolbar
        self.addToolBar(self.toolBar)

        #Setup Menubar
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&Project")
        open_action = QtWidgets.QAction("&Open",self)
        open_action.setShortcut("CTRL+O")
        open_action.triggered.connect(self.load_project)
        filemenu.addAction(open_action)
        self.addAction(open_action)


        self.show()

    def loop(self):
        self.centralWidget().stage.canvas.update()

    def closeEvent(self, event):
        bindings._game_thread.stop()

    def load_project(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self,"Open Project",".","Python (*.py)")
        if file_path[0]:
            self.centralWidget().editor.file.open(file_path[0])

def init(screen):
    global main_window, app
    app = QtWidgets.QApplication([])
    app.setApplicationName("Easypie")
    app.setOrganizationName("IT4Kids")
    app.setOrganizationDomain("it-for-kids.org")
    main_window = MainWindow(screen)


def loop():
    main_window.loop()
