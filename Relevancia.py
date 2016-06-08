# -*- coding: utf-8 -*-

from pymongo import *
from math import *

mongoClient = MongoClient('52.208.8.144', 8080)

def get_relevancia(user, ofertas):
    ofertas = __calcula_relevancia(user, ofertas)
    return ofertas

def __calcula_habilidades(user, offer):
    nota = 0
    if offer.get("imprescindible") is not None:
        for requisitos in offer.get("imprescindible"):
            nota += user.get("habilidades")[requisitos]
    return nota

def __calcula_competencias(user, offer):
    nota = 0
    if offer.get("competencias") is not None:
        for requisitos in offer.get("competencias"):
            if requisitos in user.get("competencias"):
                nota += user.get("competencias")[requisitos]
    return nota

def __calcula_rango_remuneracion(user, oferta):
    remuneracion_maxima = 0
    for offer in oferta:
        if offer.get("salario_min") is not None and len(offer.get("salario_min")) > 0:
            if remuneracion_maxima < offer.get("salario_min")[0]:
                remuneracion_maxima = offer.get("salario_min")[0]
            elif len(offer.get("salario_min")) > 1:
                if "me" in offer.get("salario_min")[1]:
                    if remuneracion_maxima < (offer.get("salario_min")[0] * 12):
                        remuneracion_maxima = offer.get("salario_min")[0] * 12
    return remuneracion_maxima

def __calcula_ranking(oferta, collection):
    cadena = oferta.get("empresa").upper()
    if collection.find_one({"Nombre": {'$regex': cadena}}) is not None:
        return int(collection.find_one({"Nombre": {'$regex': cadena}})['_id'])
    else:
        return 0

def __calcula_relevancia(user, oferta):
    db = mongoClient.ranking
    collection = db.ranking
    alfa = 0.2
    beta = 0.8
    remuneracion_max = __calcula_rango_remuneracion(user, oferta)
    for offer in oferta:
        nota = (alfa * __calcula_competencias(user, offer) + beta * __calcula_habilidades(user, offer))
        if offer.get("nivel_titulacion") is not None:
            nota += offer.get("nivel_titulacion") / 10
        if not offer.get("salario_min") and offer.get("salario_min") is not None:
            if len(offer.get("salario_min")) > 0:
                if "me" in offer.get("salario_min")[1]:
                    nota += ((int(offer.get("salario_min")[0]) * 12) / remuneracion_max) + 1
                else:
                     nota += (int(offer.get("salario_min")[0]) / remuneracion_max) + 1
        else:
            nota += 1
        nota += (1 / (log10(__calcula_ranking(offer, collection) + 1) + 2))
        offer["nota_user"] = nota
    return oferta

