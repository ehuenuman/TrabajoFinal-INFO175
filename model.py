# -*- coding: utf-8 -*-
"""
Ejemplo simple de aplicación de un diagrama de clases.
Las clases representan a las entidades, las cuales a su vez
son tablas en la base de datos.
La ventaja de las clases es que además de los atributos poseen
métodos que facilitan las consultas y ĺas centralizan.
Con esto ya se puede tener una patrón de diseño MVC.
**ADVERTENCIA:**
Este ejemplo carece de varias consideraciones que habría que tomar
al realizar una aplicación real, especialmente una APP de escritorio
que admita varios hilos de ejecución.

TODO:
    - Mantener consistencia de objetos con la BD.
    - En este esquema todavía no se pueden hacer consultas complejas (Join).
    - Clase Base que represente a una tabla genérica con los métodos Insert,
    Update, delete y load.
    - Manejar restricciones de BD a nivel de clases.
    - Cualquier cambio estructural (atributos/columnas) en las clases hay que
    replicarlo (con sentencias SQL) en la base de datos.
    - Etc.
"""
import sqlite3


def connect():
    """Retorna una conexión con la base de datos"""
    conn = sqlite3.connect('SeptimoArte.db')
    conn.row_factory = sqlite3.Row
    return conn


def last_id(conn):
    """Retorna la última primary key generada en la base de datos"""
    result = conn.execute("SELECT last_insert_rowid()")
    return result.fetchone()


class Actor(object):
    """
    Clase que representa a la tabla cursos
    Una instancia de esta clase representa a una fila.
    La instancia (objeto) puede estar en BD o no.
    El método save de la clase inserta o actualiza el registro según
    corresponda.
    Los atributos de la clase deben tener correspondencia con la BD
    (Nombres y tipos de datos)
    """
    __tablename__ = "actor"
    id_actor = None  # Primary Key
    nombre = ""
    nacimiento = ""
    genero = ""
    imagen = ""

    def __init__(
            self,
            id_actor=None,
            nombre=None,
            nacimiento="",
            genero="",
            imagen=""):

        self.id_actor = id_actor
        self.nombre = nombre
        self.nacimiento = nacimiento
        self.genero = genero
        self.imagen = imagen

        # Si la pk tiene valor hay que traer el objeto (Fila) de la DB
        if id_actor is not None:
            self.load()
        elif nombre is not None:
            self.load(nombre=nombre)

    def load(self, nombre=None):
        """
        Carga un actor de la base de datos por id_actor o nombre
        """
        conn = connect()
        query = "SELECT * FROM actor"
        if nombre is not None:
            query += " WHERE nombre = ?"
            condition = nombre
        else:
            if self.id_actor is None:
                return
            query += " WHERE id_actor = ?"
            condition = self.id_actor

        result = conn.execute(
            query, [condition])
        row = result.fetchone()
        conn.close()

        if row is not None:
            self.id_actor = row[0]
            self.nombre = row[1]
            self.nacimiento = row[2]
            self.genero = row[3]
            self.imagen = row[4]
        else:
            self.id_curso = None
            #print "El registro no existe"

    def save(self):
        """
        Guarda el objeto en la base de datos.
        Utiliza un insert o update según Corresponda
        """
        if self.id_actor is None:
            self.id_actor = self.__insert()
        else:
            self.__update()

    def __insert(self):
        query = "INSERT INTO {0} ".format(self.__tablename__)
        # La pk está definida como auto increment en el modelo
        query += "(nombre, nacimiento, genero, imagen) "
        query += "VALUES (?, ?, ?, ?)"
        try:
            conn = connect()
            result = conn.execute(
                query, [
                    self.nombre,
                    self.nacimiento,
                    self.genero,
                    self.imagen])
            conn.commit()
            id_actor = last_id(conn)
            conn.close()
            return id_actor
        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return None

    def __update(self):
        query = "UPDATE {} ".format(self.__tablename__)
        query += "SET nombre = ?, "
        query += "nacimiento = ?, "
        query += "genero = ?, "
        query += "imagen = ? "
        query += "WHERE id_actor = {}".format(self.id_actor)

        try:
            conn = connect()
            conn.execute(
                query, [
                    self.nombre,
                    self.nacimiento,
                    self.genero,
                    self.imagen])
            conn.commit()
            conn.close()
            return True

        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return False

    def delete(self):
        query = "DELETE FROM {} ".format(self.__tablename__)
        query += "WHERE id_actor = ?"
        try:
            conn = connect()
            conn.execute(query, [self.id_actor])
            conn.commit()
            conn.close()
            return True

        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return False

    @classmethod
    def actores(cls, pkActor):
        """
        Busca en la base de datos la información de varios actores.
        Desde una lista con los PK de los actores realiza la busqueda generando
        una nueva lista con la info de dichos actores.

        @param pkActor:
            Lista de los Promary Key de los actores a consultar.
        @return data:
            Lista donde esta almacenada la información de todos los actores
            consultados.
        """
        data = list()

        for i in pkActor:
            query = "SELECT * FROM {}".format(cls.__tablename__)
            query += " WHERE id_actor = {}".format(i)

            conn = connect()
            result = conn.execute(query)
            actor = result.fetchall()
            data.append(actor)

        return data

    @classmethod
    def all(cls):
        """
        Método utlizado para obtener la colección completa de filas
        en la tabla cursos.
        Este método al ser de clase no necesita una instancia (objeto)
        Sólo basta con invocaractoresDePelicula()lo desde la clase
        """
        query = "SELECT * FROM {}".format(cls.__tablename__)
        try:
            conn = connect()
            result = conn.execute(query)
            data = result.fetchall()

            return data

        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return None


class Pelicula(object):

    __tablename__ = "pelicula"
    id_pelicula = None  # Primary Key
    nombre = ""
    estreno = ""
    director = ""
    pais = ""
    actores = ""
    descripcion = ""

    def __init__(
            self,
            id_pelicula=None,
            nombre="",
            estreno="",
            director="",
            pais="",
            actores="",
            descripcion=""):

        self.id_pelicula = id_pelicula
        self.nombre = nombre
        self.estreno = estreno
        self.director = director
        self.pais = pais
        self.actores = actores
        self.descripcion = descripcion

        # Si el nombre viene con un valor hay que traer la fila de la DB
        if nombre is not None:
            self.load(nombre=nombre)

    def save(self):
        """
        Guarda el objeto en la base de datos.
        Utiliza un insert o update según Corresponda
        """
        if self.id_pelicula is None:
            self.id_pelicula = self.insert()
        else:
            pass

    def insert(self):
        query = "INSERT INTO {0} ".format(self.__tablename__)
        # La pk está definida como auto increment en el modelo
        query += "(nombre, estreno, director, pais, actores, description) "
        query += "VALUES (?, ?, ?, ?, ?, ?)"
        try:
            conn = connect()
            result = conn.execute(
                query, [
                    self.nombre,
                    self.estreno,
                    self.director,
                    self.pais,
                    self.actores,
                    self.descripcion])
            conn.commit()
#            id_actor = last_id(conn)
            conn.close()
#            return id_actor
        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return None

    def load(self, nombre=None):
        """
        Carga la información completa de una pelicula desde la base de datos
        a través del nombre e esta.
        """
        conn = connect()
        query = "SELECT * FROM pelicula"
        if nombre is not None:
            query += " WHERE nombre = ?"
            condition = nombre

        result = conn.execute(
            query, [condition])
        row = result.fetchone()
        conn.close()

        if row is not None:
            self.id_pelicula = row[0]
            self.nombre = row[1]
            self.estreno = row[2]
            self.director = row[3]
            self.pais = row[4]
            self.actores = row[5]
            self.descripcion = row[6]
        else:
            self.nombre = None
            #print "La pelicula no existe"

    @classmethod
    def peliculas(cls, pkPeliculas):
        """
        Busca en la base de datos la información de varias películas.
        Desde una lista con los PK de las películas realiza la busqueda
        generando una nueva lista con la info de dichas películas.

        @param pkPeliculas:
            Lista de los Primary Key de las películas a consultar.
        @return data:
            Lista donde esta almacenada la información de todas las películas
            consultadas.
        """
        data = list()

        for i in pkPeliculas:
            query = "SELECT * FROM {}".format(cls.__tablename__)
            query += " WHERE id_pelicula = {}".format(i)

            conn = connect()
            result = conn.execute(query)
            actor = result.fetchall()
            data.append(actor)

        return data

    @classmethod
    def all(cls):
        """
        Método utlizado para obtener la colección completa de filas
        en la tabla pelicula.
        Este método al ser de clase no necesita una instancia (objeto)
        Sólo basta con invocarlo desde la clase
        """
        query = "SELECT * FROM {}".format(cls.__tablename__)
        peliculas = list()
        try:
            conn = connect()
            result = conn.execute(query)
            data = result.fetchall()

            #for row in data:
              #  actores.append(
               #     Actor(row[0], row[1], row[2], row[3], row[4]))

            return data

        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return None


class ActorPelicula(object):

    __tablename__ = "actor_en_pelicula"
    fk_id_actor = None
    fk_id_pelicula = None
    personaje = ""
    descripcion = ""

    def __init__(
            self,
            fk_id_actor=None,
            fk_id_pelicula=None,
            personaje="",
            descripcion=""):

        self.fk_id_actor = fk_id_actor
        self.fk_id_pelicula = fk_id_pelicula
        self.personaje = personaje
        self.descripcion = descripcion

        # Si la fk_id_actor viene con valor es porque se busca las peliculas
        # en las que participo.
        # Del mismo modo si fk_id_pelicula viene con algun valor es porque
        # se busca los actores de esa película.
        if fk_id_actor is not None:
            # Buscamos Peliculas
            self.load()
        elif fk_id_pelicula is not None:
            # Buscamos Actores
            self.load(fk_id_pelicula=fk_id_pelicula)

    def save(self):
        """
        Guarda el objeto en la base de datos.
        Utiliza un insert o update según Corresponda
        """
        if self.fk_id_actor is not None:
            self.fk_id_actor = self.insert()
        else:
            print "else"
            self.__update()

    def insert(self):
        query = "INSERT INTO {0} ".format(self.__tablename__)
        # La pk está definida como auto increment en el modelo
        query += "(fk_id_actor, fk_id_pelicula, personaje, descripcion_rol) "
        query += "VALUES (?, ?, ?, ?)"
        try:
            conn = connect()
            result = conn.execute(
                query, [
                    self.fk_id_actor,
                    self.fk_id_pelicula,
                    self.personaje,
                    self.descripcion])
            conn.commit()
#            id_actor = last_id(conn)
            conn.close()
#            return id_actor
        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return None

    def __update(self):
        query = "UPDATE actor_en_pelicula"
        query += "SET fk_id_pelicula = ?, "
        query += "personaje = ?, "
        query += "descripcion_rol = ? "
        query += "WHERE fk_id_actor = ? "
        try:
            conn = connect()
            conn.execute(
                query, [
                    self.fk_id_pelicula,
                    self.personaje,
                    self.descripcion,
                    self.fk_id_actor])
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return False

    def load(self, fk_id_pelicula=None):
        """
        """
        conn = connect()
        query = "SELECT * FROM actor_en_pelicula"

        if self.fk_id_actor is not None:
            query += " WHERE fk_id_actor = ?"
            condition = self.fk_id_actor
        else:
            if fk_id_pelicula is None:
                return

            query += " WHERE fk_id_pelicula = ?"
            condition = fk_id_pelicula

        result = conn.execute(
            query, [condition])
        print result
        row = result.fetchone()
        conn.close()

        if row is not None:
            self.fk_id_actor = row[0]
            self.fk_id_pelicula = row[1]
            self.personaje = row[2]
            self.descripcion = row[3]
        else:
            self.nombre = None
            print "No existe el registro"

    @classmethod
    def actoresDeLaPelicula(cls, id_pelicula):
        """
        Retorna todas los Primary Key de los actores que participan en una
        misma pelicula buscada.

        @param id_pelicula:
            Primary Key de la película a la que le buscamos los actores.
        @return data:
            Tabla con los Primary Key de los actores participantes en la
            película buscada.
        """
        query = "SELECT fk_id_actor FROM {}".format(cls.__tablename__)
        query += " WHERE fk_id_pelicula = {}".format(id_pelicula)
        try:
            conn = connect()
            result = conn.execute(query)
            data = result.fetchall()

            return data

        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return None

    @classmethod
    def peliculasDelActor(cls, id_actor):
        """
        Retorna todas los Primary Key de las películas en las que participa el
        un mismo actor.

        @param id_actor:
            Primary Key del actor al que se le buscan las películas.
        @return data:
            Tabla con los Primary Key de las películas en las que participo el
            actor al que se le buscaban las películas.
        """
        query = "SELECT fk_id_pelicula FROM {}".format(cls.__tablename__)
        query += " WHERE fk_id_actor = {}".format(id_actor)
        try:
            conn = connect()
            result = conn.execute(query)
            data = result.fetchall()

            return data

        except sqlite3.Error as e:
            #print "A Ocurrido un Error!:", e.args[0]
            return None

    @classmethod
    def all(cls):
        """
        Método utlizado para obtener la colección completa de filas
        en la tabla actor_en_pelicula.
        Este método al ser de clase no necesita una instancia (objeto)
        Sólo basta con invocarlo desde la clase
        """
        query = "SELECT * FROM {}".format(cls.__tablename__)
        try:
            conn = connect()
            result = conn.execute(query)
            data = result.fetchall()

            return data

        except sqlite3.Error as e:
            #print "An error occurred:", e.args[0]
            return None


if __name__ == "__main__":
    """
    Ejemplos de utilización del modelo
    """
    # Obtener toda la lista de actores
    #actores = Actor.all()
    #print actores

    #actorPelicula = ActorPelicula.actoresDeLaPelicula(5)
    #print type(actorPelicula)
    #print len(actorPelicula)
    #print actorPelicula
    #row = actorPelicula[0]
    #print row[0]

    #print "---------------------------"
    #actores = Actor.actores([1, 2, 3])
    #print actores

    #print "---------------------------"
    #prueba = ActorPelicula(None, 5)
    #print prueba.fk_id_actor

    # Obtener toda la lista alumnos
    #Pelicula.all()
    # Crear un nuevo curso

    #a = Actor()
    #a.nombre = u"Hola"
    #a.nacimiento = u"Ayer"
    #a.genero = u"Femenino"
    #a.imagen = u"Ciencias de la computación.jpg"
    #a.save()
    #actores = Actor.all()
    #print actores

    #p = Pelicula()
    #p.nombre = u"a"
    #p.estreno = u"b"
    #p.director = u"c"
    #p.pais = u"d"
    #p.descripcion = u"e"
    #p.actores = u"f"
    #p.save()
    #peliculas = Pelicula.all()
    #print "-----------------------------------"
    #print peliculas
    # Actualizar un curso por codigo
    #b = Curso(codigo=u"INFO010")
    # En este momento el objeto a y b representan la misma fila en la BD
    # lo que no es correcto por que puede provocar inconsistencia!!!
    #b.nombre_curso = u"Nuevo curso editado"
    #b.save()
    # borra un curso
    #b.delete()

    # Traer todos los alumnos de un curso
    #c = Curso(1)
    #c.alumnos()
