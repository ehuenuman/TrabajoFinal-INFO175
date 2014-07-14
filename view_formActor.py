#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from formActor import Ui_FormularioActor
import controller


class FormularioActor (QtGui.QDialog):
    """
    Calse que muestra la interfaz para el formulario de actores,
    trabaja con las interacción usuario-interfaz.
    """

    def __init__(self):
        """Constructor principal de la clase FormularioActor"""
        QtGui.QDialog.__init__(self)
        self.ui = Ui_FormularioActor()
        self.ui.setupUi(self)
        self.direccion_imagen = None
        self.imagenInicial()
        self.comboBoxMeses()
        self.setSignals()

    def imagenInicial(self):
        """Setea la imagen inicial en la interfaz."""
        self.ui.imagenActorLabel.setPixmap(QtGui.QPixmap(
            "imgInterfaz/No Imagen.png"))

    def comboBoxMeses(self):
        """Rellena el ComboBox de los meses para la sección del cumpleaños."""
        meses = (
            (u"Enero"), (u"Febrero"), (u"Marzo"), (u"Abril"), (u"Mayo"),
            (u"Junio"), (u"Julio"), (u"Agosto"), (u"Septiembre"),
            (u"Octubre"), (u"Noviembre"), (u"Diciembre"))

        self.ui.mesComboBox.insertItem(0, "Mes")
        for i, data in enumerate(meses):
            self.ui.mesComboBox.insertItem(i + 1, data)

    def setSignals(self):
        """Define los eventos y sus resectivas señales."""
        self.ui.nuevaImagenButton.clicked.connect(self.examinarImagen)
        self.ui.guardarButton.clicked.connect(self.guardarActor)

    def examinarImagen(self):
        """
        Abre un nueva ventana donde le permite al usuario buscar imagenes
        *.jpg o *.png para asignarlas a un actor o película.
        """
        nueva_imagen = QtGui.QFileDialog.getOpenFileNames(self,
            "Abrir Imagenes", '', "Imagenes (*.png *.jpg)")

        try:
            self.direccion_imagen = nueva_imagen[0][0]
        except:
            self.direccion_imagen = None
        try:
            self.ui.imagenActorLabel.setPixmap(
                QtGui.QPixmap(self.direccion_imagen))
        except:
            pass

    def guardarActor(self):
        """
        Recoje todos los datos ingresados en la interfaz para pasarselos al
        controller. Donde este los revisara para luego agregarlos a la base de
        datos.
        Si existiese error en el ingreso de los datos mostrara un mensaje de
        error.
        """
        nombre = self.ui.nombreLineEdit.text()

        dia = self.ui.diaSpinBox.value()
        mes = self.ui.mesComboBox.currentText()
        year = self.ui.yearSpinBox.value()
        nacimiento = str(dia) + "|" + mes + "|" + str(year)

        masculino = self.ui.masculinoRadioButton.isChecked()
        if masculino is True:
            genero = "Masculino"
        else:
            femenino = self.ui.femeninoRadioButton.isChecked()
            if femenino is True:
                genero = "Femenino"
            else:
                genero = "No definido o.O"

        if self.direccion_imagen is None:
            imagen = "No Imagen.png"
        else:
            imagen = self.direccion_imagen

        mensaje = controller.crearActor(nombre, nacimiento, genero, imagen)
        if mensaje is not True:
            self.mensajeError(mensaje)

    def mensajeError(self, mensaje):
        """
        Función que muestra en pantalla un mensaje de error.
        @param mensaje de error
        """
        correctoQMessageBox = QtGui.QMessageBox()
        correctoQMessageBox.setWindowTitle("ERROR!")
        correctoQMessageBox.setText(mensaje)
        correctoQMessageBox.exec_()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = FormularioActor()
    window.show()
    sys.exit(app.exec_())