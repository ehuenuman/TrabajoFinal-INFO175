#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from formPelicula import Ui_FormularioPelicula
import controller


class FormularioPelicula (QtGui.QDialog):
    """
    Clase que modela muestra la interfaz para el formulario de películas,
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
        self.ui.agregarButton.clicked.connect(self.loadPelicula)
        self.ui.grabarElencoButton.clicked.connect(self.grabar)
        self.ui.cancelarButton.clicked.connect(self.reject)

    def grabar(self):
        ac = ""
        rol = self.ui.rolLineEdit.text()
        info = self.ui.infoRolPlainTextEdit.toPlainText()
        #print str(self.ui.actoresComboBox.currentText())
        ac = str(self.ui.actoresComboBox.currentText())
        actores = controller.actor()
        i = 0
        j=5
        for data in enumerate(actores):
            row = data[1]
            #print row[1]
            if ac == row[1]:
                print "son los mismos"
                print row[0]
                #controller.crearActorPelicula(row[0], j, rol, info)
            #i=i+1
        return ac

    def loadPelicula(self):
        """Carga una pelicula en la base de datos desde la interfaz"""
        #print self.ui.nombreLineEdit.text()
        #print self.ui.estrenoLineEdit.text()
        #print self.ui.directorLineEdit.text()
        #print self.ui.paisLineEdit.text()
        #print self.ui.tramaPlainTextEdit.toPlainText()
        actor = self.grabar()
        #print actor

        valido = self.ui.nombreLineEdit.text().isalpha()
        valido2 = self.ui.estrenoLineEdit.text().isdigit()
        valido3 = self.ui.directorLineEdit.text().isalpha()
        valido4 = self.ui.paisLineEdit.text().isalpha()
        valido5 = self.ui.tramaPlainTextEdit.toPlainText().isalpha()
        if(valido is False or valido2 is False or valido3 is False or valido4 is False or valido5 is False):
            correctoQMessageBox = QtGui.QMessageBox()
            correctoQMessageBox.setWindowTitle("ERROR!")
            correctoQMessageBox.setText(u"""Campo ingresado incorrectamente.
                                        \nIntente nuevamente!""")
            correctoQMessageBox.exec_()
        else:
            controller.crearPelicula(self.ui.nombreLineEdit.text(), self.ui.estrenoLineEdit.text(), self.ui.directorLineEdit.text(), self.ui.paisLineEdit.text(), self.ui.tramaPlainTextEdit.toPlainText(), actor)
            self.reject()

    def elenco(self):
        """Cambia a la pestaña elenco al presionar el botón para editarlo."""
        self.ui.stackedWidget.setCurrentIndex(1)

    def pelicula(self):
        """Cambia a la pestaña peliculas al terminar de agregar el elenco."""
        self.ui.stackedWidget.setCurrentIndex(0)

    def examinarImagen(self):
        """
        Habre un neva ventana donde le permite al usuario buscar imagenes
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