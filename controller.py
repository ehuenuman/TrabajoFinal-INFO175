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
    return Actor.all()


def pelicula():
    return Pelicula.all()


def actorPelicula():
    return ActorPelicula.all()


def obtenerActor(nombre=None):
    actor = Actor(None, nombre)

    return actor


def obtenerPelicula(nombre=None):
    pelicula = Pelicula(None, nombre)

    return pelicula


def actoresDeLaPelicula(id_pelicula):
    pk = ActorPelicula.actoresDeLaPelicula(id_pelicula)
    pkActores = list()

    for i, data in enumerate(pk):
        pkActores.append(data[0])

    actores = buscarActores(pkActores)

    return actores


def buscarActores(pkActores):
    actores = Actor.actores(pkActores)

    return actores


def peliculasDelActor(id_actor):
    pk = ActorPelicula.peliculasDelActor(id_actor)
    pkPeliculas = list()
    for i, data in enumerate(pk):
        pkPeliculas.append(data[0])

    peliculas = buscarPeliculas(pkPeliculas)

    return peliculas


def buscarPeliculas(pkPeliculas):
    peliculas = Pelicula.peliculas(pkPeliculas)

    return peliculas


def crearActor(nombre, nacimiento, genero, imagen):
    """
    Método que crea un actor.
    Valida la información recibida.
    @param nombre del actor
    @param fecha de nacimiento del actor
    @genero masculino o femenino
    @imagen dirección de la imagen que contiene al actor
    """
    nuevo = Actor()

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

    nuevo.imagen = imagen

    nuevo.save()

    # Procedemos a guardar la imagen en su directorio correspondiente
    id_actor = nuevo.id_actor[0]
    nuevaImagen = "imgActor/{}".format(id_actor)
    almacenarImagen(imagen, nuevaImagen)

    return True


def almacenarImagen(origen_imagen, nuevo_nombre):
    """
    Función que guarda la imagen para utilizarla a futuro.
    @param origen_imagen Dirección de la imagen que selecciono el usuario
    @param nuevo_nombre Dirección donde almacera la imagen seleccionada
    """
    info = os.path.splitext(origen_imagen)
    extension = info[1]
    destino_imagen = "{0}{1}".format(nuevo_nombre, extension)
    shutil.copy(origen_imagen, destino_imagen)


def crearPelicula(nombre, ano, director, pais, trama, actores):
    nuevo = Pelicula()
    nuevo.nombre = nombre
    nuevo.estreno = ano
    nuevo.director = director
    nuevo.pais = pais
    nuevo.descripcion = trama
    nuevo.actores = actores
    nuevo.save()


def crearActorPelicula(id_actor, id_peli, personaje, descripcion):
    nuevo = ActorPelicula()
    nuevo.fk_id_actor = id_actor
    nuevo.fk_id_pelicula = id_peli
    nuevo.personaje = personaje
    nuevo.descripcion = descripcion
#    print nuevo.fk_id_actor
    nuevo.save()


if __name__ == "__main__":
    pass
