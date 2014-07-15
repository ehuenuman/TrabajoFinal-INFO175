#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from loginUser import Ui_LoginUser
from septimo_arte import SeptimoArte


class FormLoginUser (QtGui.QDialog):
    """
    Clase que muestra la plataforma de Login antes de mostrar la información
    de actores y peliculas.
    """

    # Usuarios registrados en el sistema. (usuario, contraseña)
    usuarios = [
        ("admin", "admin"),
        ("Esteban", "Huenuman"),
        ("Manuel", "Lavin"),
        ("Yarithza", "Bustos"),
        ("Alexis", "Garcia"),
        ("Cristian", "Rojas")]

    def __init__(self, parent=None):
        """Constructor del formulario para usuarios."""
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_LoginUser()
        self.ui.setupUi(self)

        #Señales
        self.ui.loginButton.clicked.connect(self.checkIngreso)

    def checkIngreso(self):
        """
        Función que toma los valores ingresados por el usuario y
        los verifica.
        Si el usuario existe muestra la app.
        Si el usuario no existe rechaza la solicitud y marca error.
        """
        usuario = self.ui.usuarioLineEdit.text()
        password = self.ui.passLineEdit.text()

        correcto = False
        for i, data in enumerate(self.usuarios):
            if data[0] == usuario:
                if data[1] == password:
                    correcto = True
                    break

        if correcto:
            correctoQMessageBox = QtGui.QMessageBox()
            correctoQMessageBox.setWindowTitle("LOGIN")
            correctoQMessageBox.setText(u"Identificación Correcta!")
            correctoQMessageBox.exec_()

            main = SeptimoArte()
            main.setSourceModel(main.loadTableData(main))

            self.close()

        else:
            correctoQMessageBox = QtGui.QMessageBox()
            correctoQMessageBox.setWindowTitle("ERROR!")
            correctoQMessageBox.setText(u"""Usuario y/o contraseña incorrecta.
                                        \nIntente nuevamente!""")
            correctoQMessageBox.exec_()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    main_window = FormLoginUser()
    main_window.show()
    sys.exit(app.exec_())