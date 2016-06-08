# -*- coding: utf-8 -*-
import operator

from pymongo import *
import Filtrar_ofertas
import Relevancia
import mongodb

database_ip = "52.208.8.144"
database_port = 8080
database_requisitos = "requisitos"
database_ofertas = "ofertas"
database_usuarios = "Users"


def buscar(email):
    db_user = mongodb.get_db(database_ip, database_port, database_usuarios)
    usuario_db = db_user.find_one({'email': email})
    if usuario_db is None:
        print "Usuario no encontrado"
        return
    ofertas = Relevancia.get_relevancia(usuario_db, Filtrar_ofertas.get_ofertas(usuario_db))

    ofertas = sorted(ofertas, key=operator.itemgetter("nota_user"), reverse=True)
    print "Estas son las ofertas que hemos seleccionado apra ti"
    print ""
    for offers in ofertas:
        print str(offers.get("nota_user"))+" - "+offers.get("url")
    print ""
    return
