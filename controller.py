#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Ahora que tenemos un modelo el controlador cumple el rol de ser una capa
intermedia entre la Vista y el modelo.
Su finalidad es validar los datos de entrada que envía la vista y decidir
que información enviar a ésta.
"""

from model import Actor, Pelicula, ActorPelicula


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


def crearActor(nombre, codigo, semestre, area):
    """
    Método que crea un curso. Lo correcto sería validar
    que toda la información es correcta
    Ej:
        - Semestre puede ser 1 o 2
        - Los códigos podrían tener un formato predefinido
        - Etc
    """
    nuevo = Actor()
    nuevo.nombre = nombre
    # Aquí podrían haber validaciones para el codigo
    nuevo.codigo = codigo
    nuevo.semetre = semestre
    nuevo.area = area
    nuevo.save()

if __name__ == "__main__":
    pass
