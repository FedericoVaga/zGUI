#!/usr/bin/python
"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import sys, PyZio

from PyQt4 import QtGui
from zGUI.zgui_ui import Ui_zGui

from zGUI.ZioGuiHandler import ZioGuiHandler


if __name__ == "__main__":
    if not PyZio.is_loaded():
        exit()
    PyZio.update_all_zio_objects()

    app = QtGui.QApplication(sys.argv)
    zGui = QtGui.QMainWindow()
    ui = Ui_zGui()
    ui.setupUi(zGui)
    handle_ui = ZioGuiHandler(ui)
    zGui.show()

    sys.exit(app.exec_())
    pass
