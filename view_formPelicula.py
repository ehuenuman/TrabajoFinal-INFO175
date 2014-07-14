#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from formPelicula import Ui_FormularioPelicula
import controller


class FormularioPelicula (QtGui.QDialog):
    """
    Clase que muestra la interfaz para el formulario de películas,
    trabaja con la interacción usuario-interfaz.
    """
    def __init__(self):
        """
        Constructor del la nueva película
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_FormularioPelicula()
        self.ui.setupUi(self)
        self.imagenInicial()
        self.comboBoxActor()
        self.setSignals()

    def imagenInicial(self):
        self.ui.imagenLabel.setPixmap(QtGui.QPixmap(
            "imgInterfaz/No Imagen.png"))

    def comboBoxActor(self):
        actores = controller.actor()
        self.ui.actoresComboBox.insertItem(0, u"Seleccione Actor")
        for i, data in enumerate(actores):
            self.ui.actoresComboBox.insertItem(i + 1, data[1])

    def setSignals(self):
        self.ui.elencoButton.clicked.connect(self.elenco)
        self.ui.terminarElencoButton.clicked.connect(self.pelicula)
        self.ui.nuevaImagenButton.clicked.connect(self.examinarImagen)

    def elenco(self):
        """Cambia a la pestaña elenco al presionar el botón para editarlo."""
        self.ui.stackedWidget.setCurrentIndex(1)

    def pelicula(self):
        """Cambia a la pestaña peliculas al terminar de agregar el elenco."""
        self.ui.stackedWidget.setCurrentIndex(0)

    def examinarImagen(self):
        """
        Habre un nueva ventana donde le permite al usuario buscar imagenes
        *.jpg o *.png para asignarlas a un actor o película.
        """
        nueva_imagen = QtGui.QFileDialog.getOpenFileNames(self,
            "Abrir Imagenes", '', "Imagenes (*.png *.jpg)")

        try:
            self.direccion_imagen = nueva_imagen[0][0]
        except:
            self.direccion_imagen = None
        try:
            self.ui.imagenLabel.setPixmap(QtGui.QPixmap(self.direccion_imagen))
        except:
            pass
        try:
            self.edit.setImageLabel(self.direccion_imagen)
        except:
            pass

    def almacenarImagen(self, origen_imagen, nuevo_nombre):
        """Funcion que guarda la imagen
        @param origen_imagen,nuevo_nombre"""
        info = os.path.splitext(origen_imagen)
        extencion = info[1]
        destino_imagen = "ImgProductos/{0}{1}".format(nuevo_nombre, extencion)
        shutil.copy(origen_imagen, destino_imagen)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = FormularioPelicula()
    window.show()
    sys.exit(app.exec_())