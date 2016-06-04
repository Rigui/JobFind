# -*- coding: utf-8 -*-
from pymongo import MongoClient


def get_db():
    client = MongoClient('52.208.8.144', 27017)
    ofertasdb = client.get_database('ofertas')
    db = ofertasdb['ofertas']
    return db


def add_update_oferta(db, oferta):
    db.save(oferta)


def get_oferta(db, query=None):
    if query is None:
        query = {}
    return db.find(query)
