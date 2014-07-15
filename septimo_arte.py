#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from mainWindow import Ui_MainWindow
from view_formActor import FormularioActor
from view_formPelicula import FormularioPelicula
import controller
import sys
import os


class SeptimoArte(QtGui.QWidget):
    """Clase principal de programa."""
    columna_actor = (
        (u"Nombre", 150),
        (u"Cumpleaños", 130),
        (u"Genero", 90),
        (u"N° Películas", 90))

    columna_pelicula = (
        (u"Nombre", 200),
        (u"Estreno", 70),
        (u"Director", 150),
        (u"Pais", 80),
        (u"N° Actores", 90))

    def __init__(self):
        """Constructor principal."""
        super(SeptimoArte, self).__init__()
        self.tipoModel = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.centerWindow()
        self.setModel()
        self.setSignals()
        self.show()

        # Signals para cargar la grilla correspondiente al cambiar de Tab
        self.ui.tabWidget.currentChanged.connect(self.changedTab)

    def centerWindow(self):
        """Funcion que centra la interfaz grafica en la pantalla del usuario."""
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setModel(self):
        """Define el módelo de la grilla para trabajarla."""
        self.proxyModelActor = QtGui.QSortFilterProxyModel()
        self.proxyModelActor.setDynamicSortFilter(True)

        self.ui.actoresTreeView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.ui.actoresTreeView.setModel(self.proxyModelActor)

        self.proxyModelMovie = QtGui.QSortFilterProxyModel()
        self.proxyModelMovie.setDynamicSortFilter(True)

        self.ui.peliculasTreeView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.ui.peliculasTreeView.setModel(self.proxyModelMovie)

    def setSourceModel(self, model):
        """
        Actualiza constantemente el origen de los datos para siempre tenerlos
        al día así pudiendo buscar y mostrar solo algunos datos.
        Además llama a las funciones que rellenan los comboBox de filtrado y
        asigna el tamaño de las columnas a las grillas respectivas.
        Trabaja solo en una grilla a la vez, para esto reconoce en que Tab se
        encuentra para solamente modificar los datos de esa grilla.
        """
        indexTab = self.ui.tabWidget.currentIndex()
        # Grilla de actores
        if indexTab is 0:
            self.proxyModelActor.setSourceModel(model)

            # Designamos los header de la grilla y sus respectivos anchos
            for col, h in enumerate(self.columna_actor):
                model.setHeaderData(col, QtCore.Qt.Horizontal, h[0])
                self.ui.actoresTreeView.setColumnWidth(col, h[1])

            self.ui.buscarAPeliculaComboBox.clear()
            self.comboBoxTabActor()
            self.ui.buscarANombreLineEdit.clear()
        # Grilla de películas
        else:
            self.proxyModelMovie.setSourceModel(model)

            # Designamos los header de la grilla y sus respectivos anchos
            for col, h in enumerate(self.columna_pelicula):
                model.setHeaderData(col, QtCore.Qt.Horizontal, h[0])
                self.ui.peliculasTreeView.setColumnWidth(col, h[1])

            self.ui.buscarPActorComboBox.clear()
            self.comboBoxTabPeliculas()
            self.ui.buscarPNombreLineEdit.clear()

    def loadTableData(self, parent):
        """
        Llama a los métodos respectivos para llenar ambas grillas en la app.
        Reconoce cual es la grilla que se quiere ver para llenarla al momento
        de mostrarla.
        Para reconocer la grilla verifica en que Tab se encuentra:
            Primer Tab: Actores
            Segundo Tab: Películas
        """
        self.tipoModel = parent

        indexTab = self.ui.tabWidget.currentIndex()  # Obtiene el Tab
        if indexTab is 0:
            model = self.loadActors(parent)
        else:
            model = self.loadMovies(parent)

        return model

    def changedTab(self):
        """
        Al cambiar de Tab en la app ordena que se actualice el Tab completo
        al que nos trasladamos.
        """
        self.setSourceModel(self.loadTableData(self.tipoModel))

    def setSignals(self):
        # Signals TabActor
        self.ui.actoresTreeView.clicked.connect(self.infoClick)
        self.ui.actoresTreeView.activated.connect(self.infoClick)
        self.ui.buscarANombreLineEdit.textChanged.connect(
            self.filtrarActorNombre)
        self.ui.buscarAPeliculaComboBox.currentIndexChanged.connect(
            self.filtrarActorPorPelicula)
        self.ui.nuevoAButton.clicked.connect(self.nuevoActor)
        self.ui.editarAButton.clicked.connect(self.editarActor)
        self.ui.borrarAButton.clicked.connect(self.borrarActor)

        #Signals TabPelicula
        self.ui.peliculasTreeView.clicked.connect(self.infoClick)
        self.ui.peliculasTreeView.activated.connect(self.infoClick)
        self.ui.buscarPNombreLineEdit.textChanged.connect(
            self.filtrarPeliculaNombre)
        self.ui.buscarPActorComboBox.currentIndexChanged.connect(
            self.filtrarPeliculaPorActor)
        self.ui.nuevoPButton.clicked.connect(self.nuevaPelicula)

    ########################################################################
    #################### Estructuración del Tab Actores ####################
    ########################################################################

    def loadActors(self, parent):
        actores = controller.actor()
        row = len(actores)

        model = QtGui.QStandardItemModel(row, len(self.columna_actor), parent)

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

    def infoClick(self):
        indexTab = self.ui.tabWidget.currentIndex()
        if indexTab is 0:
            # Estamos en el Tab Actores
            index = self.ui.actoresTreeView.currentIndex()  # n° fila tabla
            model = self.ui.actoresTreeView.model()

            nombre = model.index(index.row(), 0, QtCore.QModelIndex()).data()
            a = controller.obtenerActor(nombre)

            imagenes = os.listdir("imgActor/")
            foto = str(a.id_actor) + ".jpg" in imagenes
            if foto is True:
                direccion = "imgActor/{}".format(str(a.id_actor) + ".jpg")
            else:
                foto = str(a.id_actor) + ".png" in imagenes
                if foto is True:
                    direccion = "imgActor/{}".format(str(a.id_actor) + ".png")
                else:
                    direccion = "imgInterfaz/NoImagenActor.png"

            self.ui.actorImagenLabel.setPixmap(QtGui.QPixmap(direccion))

        else:
            # Estamos en el Tab Películas
            index = self.ui.peliculasTreeView.currentIndex()  # n° fila tabla
            model = self.ui.peliculasTreeView.model()

            nombre = model.index(index.row(), 0, QtCore.QModelIndex()).data()
            p = controller.obtenerPelicula(nombre)

            imagenes = os.listdir("imgPelicula/")
            caratula = str(p.id_pelicula) + ".jpg" in imagenes
            if caratula is True:
                direccion = "imgPelicula/{}".format(str(p.id_pelicula) + ".jpg")
            else:
                direccion = "imgPelicula/{}".format(str(p.id_pelicula) + ".png")

            self.ui.peliculaImagenLabel.setPixmap(QtGui.QPixmap(direccion))

            self.ui.tramaPLabel.setText(p.descripcion)

    def filtrarActorNombre(self):
        self.ui.actorImagenLabel.setPixmap(QtGui.QPixmap(""))  # Oculta la img

        self.proxyModelActor.setFilterKeyColumn(0)
        regExp = QtCore.QRegExp(self.ui.buscarANombreLineEdit.text(),
                QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)

        self.proxyModelActor.setFilterRegExp(regExp)

    def filtrarActorPorPelicula(self):
        self.ui.actorImagenLabel.setPixmap(QtGui.QPixmap(""))

        index = self.ui.buscarAPeliculaComboBox.currentIndex()

        if (index != 0):
            nombre = self.ui.buscarAPeliculaComboBox.itemText(index)
            pelicula = controller.obtenerPelicula(nombre)  # Info de la pelicula
            actores = controller.actoresDeLaPelicula(pelicula.id_pelicula)
            actoresAFiltrar = ""

            if actores is not None:
                for i, data in enumerate(actores):
                    row = data[0]
                    if i == len(actores) - 1:
                        actoresAFiltrar += row[1]
                    else:
                        actoresAFiltrar += row[1] + "|"

            if actoresAFiltrar is "":
                actoresAFiltrar = u"@~@"

        else:
            self.proxyModelActor.setFilterKeyColumn(0)
            actoresAFiltrar = u'|'

        actoresFiltrados = QtCore.QRegExp(
            actoresAFiltrar, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.proxyModelActor.setFilterRegExp(actoresFiltrados)

    def nuevoActor(self):
        form = FormularioActor()
        form.exec_()
        self.setSourceModel(self.loadTableData(self.tipoModel))

    def editarActor(self):
        """
        """
        index = self.ui.actoresTreeView.currentIndex()  # n° fila tabla
        if index.row() == -1:
            mensaje = "Debe de seleccionar una fila"
            errorQMessageBox = QtGui.QMessageBox()
            errorQMessageBox.setWindowTitle("ERROR!")
            errorQMessageBox.setText(mensaje)
            errorQMessageBox.exec_()
        else:
            model = self.ui.actoresTreeView.model()
            nombre = model.index(index.row(), 0, QtCore.QModelIndex()).data()
            a = controller.obtenerActor(nombre)

            form = FormularioActor(a.id_actor)
            form.exec_()
            self.setSourceModel(self.loadTableData(self.tipoModel))

    def borrarActor(self):
        index = self.ui.actoresTreeView.currentIndex()  # n° fila tabla
        if index.row() == -1:
            mensaje = "Debe de seleccionar una fila"
            errorQMessageBox = QtGui.QMessageBox()
            errorQMessageBox.setWindowTitle("ERROR!")
            errorQMessageBox.setText(mensaje)
            errorQMessageBox.exec_()
        else:
            model = self.ui.actoresTreeView.model()
            nombre = model.index(index.row(), 0, QtCore.QModelIndex()).data()
            a = controller.obtenerActor(nombre)
            borrado = controller.borrarActor(a)

            if borrado is True:
                mensaje = "Actor borrado correctamente"
                errorQMessageBox = QtGui.QMessageBox()
                errorQMessageBox.setWindowTitle("Borrado!")
                errorQMessageBox.setText(mensaje)
                errorQMessageBox.exec_()
                self.setSourceModel(self.loadTableData(self.tipoModel))

    ########################################################################
    ################### Estructuración del Tab Películas ###################
    ########################################################################

    def loadMovies(self, parent):
        """
        Carga desde la base de datos todas las peliculas y su información a la
        grilla del TabActores.
        """
        peliculas = controller.pelicula()
        row = len(peliculas)

        model = QtGui.QStandardItemModel(row,
            len(self.columna_pelicula), parent)

        for i, data in enumerate(peliculas):
            row = [data[1], data[2], data[3], data[4]]
            for j, field in enumerate(row):
                index = model.index(i, j, QtCore.QModelIndex())
                model.setData(index, field)

        return model

    def comboBoxTabPeliculas(self):
        """
        Rellena el comboBox que se ubica en el Tab Peliculas (secundario)
        con todos los actores que se encuentran en la base de datos para luego
        utilizarlos para filtrar el contenido de la grilla.
        """
        actores = controller.actor()
        self.ui.buscarPActorComboBox.insertItem(0, u"Todos")
        for i, data in enumerate(actores):
            self.ui.buscarPActorComboBox.insertItem(i + 1, data[1])

    def filtrarPeliculaNombre(self):
        """
        Filtra por nombre de la película mientras se va escribiendo en el
        lineEdit.
        """
        self.ui.peliculaImagenLabel.setPixmap(QtGui.QPixmap(""))
        self.ui.tramaPLabel.clear()
        #self.ui.buscarPActorComboBox.setCurrentIndex(0)

        self.proxyModelMovie.setFilterKeyColumn(0)
        regExp = QtCore.QRegExp(self.ui.buscarPNombreLineEdit.text(),
                QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)

        self.proxyModelMovie.setFilterRegExp(regExp)

    def filtrarPeliculaPorActor(self):
        """
        Filtra las películas por el actor que participo en ellas luego de
        seleccionar dicho actor desde el comboBox en el Tab de las Películas.
        """
        self.ui.peliculaImagenLabel.setPixmap(QtGui.QPixmap(""))
        self.ui.tramaPLabel.clear()
        #self.ui.buscarPNombreLineEdit.clear()

        index = self.ui.buscarPActorComboBox.currentIndex()
        if (index != 0):
            nombre = self.ui.buscarPActorComboBox.itemText(index)
            actor = controller.obtenerActor(nombre)  # Info del Actor
            peliculas = controller.peliculasDelActor(actor.id_actor)
            peliculasAFiltrar = ""

            if peliculas is not None:
                for i, data in enumerate(peliculas):
                    row = data[0]
                    if i == len(peliculas) - 1:
                        peliculasAFiltrar += row[1]
                    else:
                        peliculasAFiltrar += row[1] + "|"

            if peliculasAFiltrar is "":
                peliculasAFiltrar = u"@~@"

        else:
            self.proxyModelMovie.setFilterKeyColumn(0)
            peliculasAFiltrar = u'|'

        peliculasFiltradas = QtCore.QRegExp(
            peliculasAFiltrar, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.proxyModelMovie.setFilterRegExp(peliculasFiltradas)

    def nuevaPelicula(self):
        form = FormularioPelicula()
        form.exec_()
        self.setSourceModel(self.loadTableData(self.tipoModel))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = SeptimoArte()
    main.setSourceModel(main.loadTableData(main))
    sys.exit(app.exec_())
