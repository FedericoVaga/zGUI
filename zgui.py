"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import sys

from PyQt4 import QtGui
from zGUI.zgui_ui import Ui_zGui

from zGUI.zgui_ui_handler import ui_handler
from PyZio import zUtil


if __name__ == "__main__":
    if not zUtil.isLoaded():
        exit()
    zUtil.updateAll()

    app = QtGui.QApplication(sys.argv)
    zGui = QtGui.QMainWindow()
    ui = Ui_zGui()
    ui.setupUi(zGui)
    handle_ui = ui_handler(ui)
    zGui.show()

    sys.exit(app.exec_())
    pass
