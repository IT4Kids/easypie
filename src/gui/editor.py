# coding=utf-8
import sys

from pyqode.core import modes, panels, api
from pyqode.core.api import ColorScheme
from pyqode.python import modes as pymodes
from pyqode.python import panels as pypanels
from pyqode.core.widgets import SplittableCodeEditTabWidget
from pyqode.python.backend import server, defined_names
from pyqode.python.folding import PythonFoldDetector
from pyqode.python.widgets import PyCodeEditBase

import signals


class MyCodeEdit(PyCodeEditBase):
    """
    Extends PyCodeEditBase with a set of hardcoded modes and panels specifics
    to a python code editor widget.
    """
    DARK_STYLE = 0
    LIGHT_STYLE = 1

    mimetypes = ['text/x-python']

    def __init__(self, parent=None, server_script=server.__file__,
                 interpreter=sys.executable, args=None,
                 create_default_actions=True, color_scheme='monokai',
                 reuse_backend=False):
        super(PyCodeEditBase, self).__init__(
            parent=parent, create_default_actions=create_default_actions)

        if not getattr(sys, 'frozen', False):
            self.backend.start(server_script, interpreter, args,
                               reuse=reuse_backend)

        self.setLineWrapMode(self.NoWrap)
        self.setWindowTitle("pyQode - Python Editor")

        # install those modes first as they are required by other modes/panels
        self.modes.append(modes.OutlineMode(defined_names))

        # panels
        self.panels.append(panels.SearchAndReplacePanel(),
                           panels.SearchAndReplacePanel.Position.BOTTOM)
        self.panels.append(panels.FoldingPanel())
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.CheckerPanel())
        self.panels.append(panels.GlobalCheckerPanel(),
                           panels.GlobalCheckerPanel.Position.RIGHT)
        self.add_separator()

        # modes
        # generic
        self.modes.append(modes.ExtendedSelectionMode())
        self.modes.append(modes.CaseConverterMode())
        self.modes.append(modes.CaretLineHighlighterMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.RightMarginMode())
        self.modes.append(modes.ZoomMode())
        self.modes.append(modes.SymbolMatcherMode())
        self.modes.append(modes.CodeCompletionMode())
        self.modes.append(modes.OccurrencesHighlighterMode())
        self.modes.append(modes.SmartBackSpaceMode())
        # python specifics
        if not getattr(sys, 'frozen', False):
            self.modes.append(pymodes.CalltipsMode())
            self.modes.append(pymodes.PyAutoCompleteMode())
            self.panels.append(pypanels.QuickDocPanel(), api.Panel.Position.BOTTOM)

        self.modes.append(pymodes.PyAutoIndentMode())
        self.modes.append(pymodes.PyFlakesChecker())
        self.modes.append(pymodes.PEP8CheckerMode())
        self.modes.append(pymodes.PyIndenterMode())
        self.modes.append(pymodes.GoToAssignmentsMode())
        self.modes.append(pymodes.CommentsMode())
        self.modes.append(pymodes.PythonSH(
            self.document(), color_scheme=ColorScheme(color_scheme)))
        self.syntax_highlighter.fold_detector = PythonFoldDetector()
        self.panels.append(panels.EncodingPanel(), api.Panel.Position.TOP)
        self.panels.append(panels.ReadOnlyPanel(), api.Panel.Position.TOP)

    def clone(self):
        clone = self.__class__(
            parent=self.parent(), server_script=self.backend.server_script,
            interpreter=self.backend.interpreter, args=self.backend.args,
            color_scheme=self.syntax_highlighter.color_scheme.name)
        return clone

    def __repr__(self):
        return 'PyCodeEdit(path=%r)' % self.file.path


class Editor(SplittableCodeEditTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.register_code_edit(MyCodeEdit)
        signals.all.save_as_signal.connect(self.save_current_as)
        signals.all.save_signal.connect(self.save_current)
        signals.all.new_signal.connect(lambda: self.create_new_document(extension=".py"))

    def save_current(self):
        if self.current_widget():
            if not self.current_widget().file.path:
                self.save_current_as()
            else:
                super().save_current()

    def get_code(self):
        if self.current_widget():
            return self.current_widget().toPlainText(), self.current_widget().file.path
        return "", ""
