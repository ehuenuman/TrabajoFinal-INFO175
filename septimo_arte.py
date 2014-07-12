#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from mainWindow import Ui_MainWindow
from view_formPelicula import FormularioPelicula
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
        """Constructor principal."""
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
        """
        Funcion que centra la interfaz grafica en la pantalla del usuario.
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setModel(self):
        """
        Define el módelo de la grilla para trabajarla.
        """
        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)

        self.ui.actoresTreeView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.ui.actoresTreeView.setModel(self.proxyModel)

    def setSourceModel(self, model):
        """
        Actualiza constantemente el origen de los datos para siempre tenerlos
        al día así pudiendo buscar y mostrar solo algunos datos.
        """
        self.proxyModel.setSourceModel(model)

    def loadTableData(self, parent):
        """
        Llama a los métodos respectivos para llenar ambas grillas en la app.

        """
        self.tipoModel = parent
        model = self.loadActors(parent)

        return model

    #***********************************************************************
    # Estructuración del tab Actores
    #***********************************************************************

    def loadActors(self, parent):
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
        """
        Rellena el comboBox que se ubica en el Tab Actor (principal) con todas
        las películas que se encuentran en la base de datos para luego
        utilizarlas para filtrar el contenido de la grilla.
        """
        peliculas = controller.pelicula()
        self.ui.buscarAPeliculaComboBox.insertItem(0, u"Todas")
        for i, data in enumerate(peliculas):
            self.ui.buscarAPeliculaComboBox.insertItem(i + 1, data[1])

    def setSignals(self):
        self.ui.actoresTreeView.clicked.connect(self.infoClick)
        self.ui.actoresTreeView.activated.connect(self.infoClick)
        self.ui.buscarANombreLineEdit.textChanged.connect(
            self.filtrarActorNombre)
        self.ui.buscarAPeliculaComboBox.currentIndexChanged.connect(
            self.filtrarActorPelicula)
        self.ui.nuevoAButton.clicked.connect(self.nuevoActor)

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
        self.ui.actorImagenLabel.setPixmap(QtGui.QPixmap(""))  # Oculta la img
        self.proxyModel.setFilterKeyColumn(0)
        regExp = QtCore.QRegExp(self.ui.buscarANombreLineEdit.text(),
                QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)

        self.proxyModel.setFilterRegExp(regExp)

    def filtrarActorPelicula(self, parent):
        self.ui.actorImagenLabel.setPixmap(QtGui.QPixmap(""))
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

    def nuevoActor(self):
        form = FormularioPelicula()
        form.exec_()
        self.setSourceModel(self.loadTableData(self.tipoModel))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = SeptimoArte()
    main.setSourceModel(main.loadTableData(main))
    sys.exit(app.exec_())
