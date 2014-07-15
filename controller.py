#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Ahora que tenemos un modelo el controlador cumple el rol de ser una capa
intermedia entre la Vista y el modelo.
Su finalidad es validar los datos de entrada que envía la vista y decidir
que información enviar a ésta.
"""

from model import Actor, Pelicula, ActorPelicula
import shutil
import os


def actor():
    """Retorna a todos los actores y sus datos"""
    return Actor.all()


def pelicula():
    """Retorna a todas las películas y sus datos"""
    return Pelicula.all()


def actorPelicula():
    """Retorna la relación n a n de actores y películas"""
    return ActorPelicula.all()


def obtenerActor(nombre=None):
    """Retorna un actor (objeto) liego de buscarlo a traves de su nombre"""
    actor = Actor(None, nombre)

    return actor


def obtenerActorId(idActor):
    """Returna un actor (objeto) luego de buscarlo a traves de su id_actor"""
    actor = Actor(idActor)

    return actor


def obtenerPelicula(nombre=None):
    """Retorna una pelicula (objeto) luego de buscarla a traves de su nombre"""
    pelicula = Pelicula(None, nombre)

    return pelicula


def actoresDeLaPelicula(id_pelicula):
    """
    Busca a todos los actores que participaron en la misma pelicula.
    Retorna la información como una lista."""
    pk = ActorPelicula.actoresDeLaPelicula(id_pelicula)
    pkActores = list()

    if pk is not None:
        for i, data in enumerate(pk):
            pkActores.append(data[0])

        actores = buscarActores(pkActores)

        return actores


def buscarActores(pkActores):
    """
    Busca a más de un actor y su información desde una lista con las Pk de
    los actores que se desean buscar.
    """
    actores = Actor.actores(pkActores)

    return actores


def peliculasDelActor(id_actor):
    """
    Busca todas las películas de un mismo actor a traves de la PK del actor.
    """
    pk = ActorPelicula.peliculasDelActor(id_actor)
    pkPeliculas = list()
    if pk is not None:
        for i, data in enumerate(pk):
            pkPeliculas.append(data[0])

        peliculas = buscarPeliculas(pkPeliculas)

        return peliculas


def buscarPeliculas(pkPeliculas):
    """
    Busca más de una película y su informació. Esto lo logra reciviendo una
    lista con todas las Pk de las películas que se desean buscar.
    """
    peliculas = Pelicula.peliculas(pkPeliculas)

    return peliculas


def crearActor(id_actor, nombre, nacimiento, genero):
    """
    Método que crea un actor.
    Valida la información recibida.
    @param nombre del actor
    @param fecha de nacimiento del actor
    @genero masculino o femenino
    """
    nuevo = Actor()

    nuevo.id_actor = id_actor

    if len(nombre.strip()) is 0:
        mensaje = u"Ingrese nombre del actor"
        return mensaje
    if nombre.strip().replace(" ", "").isalpha() is False:
        mensaje = u"Nombre del actor no valido"
        return mensaje
    nombre = nombre.strip()
    nuevo.nombre = nombre

    if "Mes" in nacimiento:
        mensaje = u"Ingrese mes de cumpleaños."
        return mensaje
    nuevo.nacimiento = nacimiento

    if "No definido o.O" in genero:
        mensaje = u"Especifique el genero del actor"
        return mensaje
    nuevo.genero = genero
    nuevo.save()

    return True


def borrarActor(actor):
    """Borra toda la información de un actor."""
    id_actor = actor.id_actor

    borrado = actor.delete()

    imagenes = os.listdir("imgActor/")
    foto = str(id_actor) + ".jpg" in imagenes
    if foto is True:
        imagen = "imgActor/{0}{1}".format(id_actor, ".jpg")
        os.remove(imagen)
    else:
        imagen = "imgActor/{0}{1}".format(id_actor, ".png")
        os.remove(imagen)

    return borrado


def crearPelicula(nombre, ano, director, pais, trama, actores):
    """
    Recibiendo todos los datos ingresados en el formulario, crea un nuevo
    objeto pelicula y setea la información.
    """
    nuevo = Pelicula()
    nuevo.nombre = nombre
    nuevo.estreno = ano
    nuevo.director = director
    nuevo.pais = pais
    nuevo.descripcion = trama
    nuevo.actores = actores
    nuevo.save()


def crearActorPelicula(id_actor, id_peli, personaje, descripcion):
    """
    Crea una nueva relacion para actor y película"
    """
    nuevo = ActorPelicula()
    nuevo.fk_id_actor = id_actor
    nuevo.fk_id_pelicula = id_peli
    nuevo.personaje = personaje
    nuevo.descripcion = descripcion
#    print nuevo.fk_id_actor
    nuevo.save()


def almacenarImagen(origen_imagen, nuevo_nombre):
    """
    Función que guarda la imagen para utilizarla a futuro.
    @param origen_imagen Dirección de la imagen que selecciono el usuario
    @param nuevo_nombre Dirección donde almacera la imagen seleccionada
    """
    info = os.path.splitext(origen_imagen)
    extension = info[1]
    destino_imagen = "{0}{1}".format(nuevo_nombre, extension)
    if origen_imagen == destino_imagen:
        pass
    else:
        shutil.copy(origen_imagen, destino_imagen)


if __name__ == "__main__":
    #actor = obtenerActorId(1)
    #print actor.id_actor
    #print actor.nombre
    #print actor.nacimiento.split("|")
    pass
