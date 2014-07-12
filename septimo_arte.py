#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from mainWindow import Ui_MainWindow
from model import Actor, Pelicula, ActorPelicula
import controller
import sys


class SeptimoArte(QtGui.QWidget):
    """Clase principal de programa."""
    columnas_actor = (
        (u"Nombre", 200),
        (u"Cumpleaños", 100),
        (u"Genero", 100),
        (u"N° Películas", 50))

    def __init__(self):
        "Constructor principal."
        super(SeptimoArte, self).__init__()
        self.tipoModel = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.centerWindow()
        self.setModel()
        #self.loadMovies()
        self.setSignals()
        self.show()

    def centerWindow(self):
        """Funcion que centra la interfaz grafica en la pantalla"""
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setModel(self):
        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)

        self.ui.actoresTreeView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.ui.actoresTreeView.setModel(self.proxyModel)

    def loadActors(self, parent):
        #self.tipoModel = parent
        self.comboBoxTabActor()
        actores = controller.actor()
        row = len(actores)

        model = QtGui.QStandardItemModel(row, len(self.columnas_actor), parent)

        for col, h in enumerate(self.columnas_actor):
            model.setHeaderData(col, QtCore.Qt.Horizontal, h[0])
            self.ui.actoresTreeView.setColumnWidth(col, h[1])

        for i, data in enumerate(actores):
            row = [data[1], data[2], data[3]]
            for j, field in enumerate(row):
                index = model.index(i, j, QtCore.QModelIndex())
                model.setData(index, field)

        return model

    def comboBoxTabActor(self):
        peliculas = controller.pelicula()
        self.ui.buscarAPeliculaComboBox.insertItem(0, u"Todas")
        for i, data in enumerate(peliculas):
            self.ui.buscarAPeliculaComboBox.insertItem(i + 1, data[1])

    def setSourceModel(self, model):
        self.proxyModel.setSourceModel(model)

    def setSignals(self):
        self.ui.actoresTreeView.clicked.connect(self.infoClick)
        self.ui.actoresTreeView.activated.connect(self.infoClick)
        self.ui.buscarANombreLineEdit.textChanged.connect(
            self.filtrarActorNombre)
        self.ui.buscarAPeliculaComboBox.currentIndexChanged.connect(
            self.filtrarActorPelicula)

    def infoClick(self):
        indexTab = self.ui.tabWidget.currentIndex()
        index = self.ui.actoresTreeView.currentIndex()  # n° fila tabla
        model = self.ui.actoresTreeView.model()
        if indexTab is 0:
            #Estamos en el tab Actores
            nombre = model.index(index.row(), 0, QtCore.QModelIndex()).data()
            a = controller.obtenerActor(nombre)

            direccion = "imgActor/{0}".format(a.imagen)
            self.ui.actorImagenLabel.setPixmap(QtGui.QPixmap(direccion))

        else:
            #Estamos en el tab Películas
            pass

    def filtrarActorNombre(self):
        self.proxyModel.setFilterKeyColumn(0)
        regExp = QtCore.QRegExp(self.ui.buscarANombreLineEdit.text(),
                QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)

        self.proxyModel.setFilterRegExp(regExp)

    def filtrarActorPelicula(self, parent):
        index = self.ui.buscarAPeliculaComboBox.currentIndex()

        if (index != 0):
            nombre = self.ui.buscarAPeliculaComboBox.itemText(index)

            pelicula = controller.obtenerPelicula(nombre)  # Info de la pelicula

            actores = controller.actoresDePelicula(pelicula.id_pelicula)

            actoresAFiltrar = ""

            for i, data in enumerate(actores):
                row = data[0]
                if i == len(actores) - 1:
                    actoresAFiltrar += row[1]
                else:
                    actoresAFiltrar += row[1] + "|"

            if actoresAFiltrar is "":
                actoresAFiltrar = u"@"

        else:
            self.proxyModel.setFilterKeyColumn(0)
            actoresAFiltrar = u'|'

        actoresFiltrados = QtCore.QRegExp(
            actoresAFiltrar, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.proxyModel.setFilterRegExp(actoresFiltrados)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = SeptimoArte()
    main.setSourceModel(main.loadActors(main))
    sys.exit(app.exec_())
