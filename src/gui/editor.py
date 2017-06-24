# coding=utf-8
from pyqode.python.modes import PEP8CheckerMode, CalltipsMode
from pyqode.python.panels import QuickDocPanel
from pyqode.core.modes import CodeCompletionMode
from pyqode.core.widgets import SplittableCodeEditTabWidget
from pyqode.python.widgets import PyCodeEdit
import src.signals

class MyCodeEdit(PyCodeEdit):
    # https://pythonhosted.org/pyqode.python/examples.html
    def __init__(self, parent=None):
        super().__init__(parent=parent,color_scheme='monokai', autostart_backend=False)
        self.modes.remove(PEP8CheckerMode)
        self.modes.remove(CodeCompletionMode)
        self.modes.remove(CalltipsMode)
        self.panels.remove(QuickDocPanel)


class Editor(SplittableCodeEditTabWidget):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.register_code_edit(MyCodeEdit)
        self.create_new_document(base_name="NewFile",extension=".py")
        src.signals.all.save_as_signal.connect(self.save_current_as)
        src.signals.all.save_signal.connect(self.save_current)

    def save_current(self):
        if self.current_widget():
            if not self.current_widget().file.path:
                self.save_current_as()
            else:
                super().save_current()
