#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from view_loginUser import FormLoginUser

"""
Archivo que solo inicia la aplicación de una forma más limpia.
"""

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    mainWindow = FormLoginUser()
    mainWindow.show()
    sys.exit(app.exec_())
