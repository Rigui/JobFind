import pymongo
from pymongo import MongoClient, DeleteOne


def conectar():      #cambiar a la base de datos que se necesite
    client = MongoClient('52.208.8.144', 27017)
    db = client.test
    cursor = db.prueba
    return cursor

def actualizar(col,id, campoValor):     #también sirve para incluir nuevos campos mediante el parametro campoValor
    col.update({'_id':id}, {'$set': campoValor})

def eliminar(col, id):
    col.remove({"_id": id})
