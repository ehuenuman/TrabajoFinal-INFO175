#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from formActor import Ui_FormularioActor
import controller
import sys
import os


class FormularioActor (QtGui.QDialog):
    """
    Calse que muestra la interfaz para el formulario de actores,
    trabaja con las interacción usuario-interfaz.
    """
    meses = ((u"Enero"), (u"Febrero"), (u"Marzo"), (u"Abril"), (u"Mayo"),
            (u"Junio"), (u"Julio"), (u"Agosto"), (u"Septiembre"),
            (u"Octubre"), (u"Noviembre"), (u"Diciembre"))

    id_actor = None  # Primary Key
    direccion_imagen = None
    temp_direccion = ""

    def __init__(self, id_actor=None):
        """Constructor principal de la clase FormularioActor"""
        QtGui.QDialog.__init__(self)
        self.id_actor = id_actor
        self.direccion_imagen = None

        self.ui = Ui_FormularioActor()
        self.ui.setupUi(self)
        self.comboBoxMeses()
        if self.id_actor is not None:
            self.llenarFormularioEditar()
        else:
            self.imagenInicial()

        self.setSignals()

    def imagenInicial(self):
        """Setea la imagen inicial en la interfaz."""
        self.ui.imagenActorLabel.setPixmap(QtGui.QPixmap(
            "imgInterfaz/NoImagenActor.png"))

    def comboBoxMeses(self):
        """Rellena el ComboBox de los meses para la sección del cumpleaños."""
        self.ui.mesComboBox.insertItem(0, "Mes")
        for i, data in enumerate(self.meses):
            self.ui.mesComboBox.insertItem(i + 1, data)

    def llenarFormularioEditar(self):
        self.setWindowTitle("Modificar Actor")
        actor = controller.obtenerActorId(self.id_actor)

        self.ui.nombreLineEdit.setText(actor.nombre)
        nacimiento = actor.nacimiento.split("|")
        dia = int(nacimiento[0])
        self.ui.diaSpinBox.setValue(dia)
        mes = nacimiento[1].capitalize()
        for i, data in enumerate(self.meses):
            if mes in data:
                self.ui.mesComboBox.setCurrentIndex(i + 1)
        year = int(nacimiento[2])
        self.ui.yearSpinBox.setValue(year)

        if "Masculino" in actor.genero:
            self.ui.masculinoRadioButton.setChecked(True)
        else:
            self.ui.femeninoRadioButton.setChecked(True)

        imagenes = os.listdir("imgActor/")
        foto = str(self.id_actor) + ".jpg" in imagenes
        if foto is True:
            direccion = "imgActor/{}".format(str(self.id_actor) + ".jpg")
            self.temp_direccion = direccion
        else:
            foto = str(self.id_actor) + ".png" in imagenes
            if foto is True:
                direccion = "imgActor/{}".format(str(self.id_actor) + ".png")
                self.temp_direccion = direccion
            else:
                direccion = "imgInterfaz/NoImagenActor.png"

        self.ui.imagenActorLabel.setPixmap(QtGui.QPixmap(direccion))

        self.direccion_imagen = direccion

    def setSignals(self):
        """Define los eventos y sus resectivas señales."""
        self.ui.nuevaImagenButton.clicked.connect(self.examinarImagen)
        self.ui.guardarButton.clicked.connect(self.guardarActor)
        self.ui.borrarImagenButton.clicked.connect(self.borrarImagenLabel)

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
        nacimiento = str(dia) + "|" + mes.lower() + "|" + str(year)

        masculino = self.ui.masculinoRadioButton.isChecked()
        if masculino is True:
            genero = "Masculino"
        else:
            femenino = self.ui.femeninoRadioButton.isChecked()
            if femenino is True:
                genero = "Femenino"
            else:
                genero = "No definido o.O"

        mensaje = controller.crearActor(
            self.id_actor, nombre, nacimiento, genero)

        if mensaje is not True:
            self.mensajeError(mensaje)
        else:
            try:
                os.remove(self.temp_direccion)
            except:
                pass

            direccion_destino = "imgActor/{}".format(self.id_actor)
            if "imgInterfaz/NoImagenActor.png" != self.direccion_imagen:
                controller.almacenarImagen(
                    self.direccion_imagen, direccion_destino)

            mensaje = "Actor agregado satisfactoriamente."
            correctoQMessageBox = QtGui.QMessageBox()
            correctoQMessageBox.setWindowTitle("FELICIDADES!")
            correctoQMessageBox.setText(mensaje)
            correctoQMessageBox.exec_()

            self.close()

    def mensajeError(self, mensaje):
        """
        Función que muestra en pantalla un mensaje de error.
        @param mensaje de error
        """
        correctoQMessageBox = QtGui.QMessageBox()
        correctoQMessageBox.setWindowTitle("ERROR!")
        correctoQMessageBox.setText(mensaje)
        correctoQMessageBox.exec_()

    def borrarImagenLabel(self):
        direccion = "imgInterfaz/NoImagenActor.png"
        self.ui.imagenActorLabel.setPixmap(QtGui.QPixmap(direccion))

        self.direccion_imagen = direccion

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = FormularioActor()
    window.show()
    sys.exit(app.exec_())