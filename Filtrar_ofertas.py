# -*- coding: utf-8 -*-

from pymongo import *

mongoClient = MongoClient('52.208.8.144', 27017)

def get_ofertas(users):
    ofertas = __filtra_ofertas(users)
    return ofertas


def __comprueba_desplazamiento(users, oferta):
    if users.get("desplazamiento") == '0':
        if oferta.get("ciudad") is not None:
            if users.get("ciudad").lower() in oferta.get("ciudad").lower():
                return oferta
        else:
            return oferta
    elif users.get("desplazamiento") == '1':
        if oferta.get("provincia") is not None:
            if users.get("provincia").lower() in oferta.get("provincia").lower():
                return oferta
        else:
            return oferta
    elif users.get("desplazamiento") == '2':
        if oferta.get("comunidad") is not None:
            if users.get("comunidad").lower() in oferta.get("comunidad").lower():
                return oferta
        else:
            return oferta
    elif users.get("desplazamiento") == '3':
        if oferta.get("pais") is not None:
            if users.get("pais").lower() in oferta.get("pais").lower():
                return oferta
        else:
            return oferta

def __comprueba_idiomas(users, oferta, impres, find_idioma, idioma):
    if oferta.get(impres) is not None:
        imprescindible = oferta.get(impres).lower()
        if imprescindible.find(find_idioma) is not -1:
            if imprescindible.find(find_idioma) > 8:
                start = imprescindible.find(find_idioma) - 25
            else:
                start = 0
            end = imprescindible.find(find_idioma) + 25
            cadena = imprescindible[start: end]
            if users.get("idiomas").has_key(idioma):
                nivel_user = int(users.get("idiomas")[idioma])
                nivel_oferta = 10
                if cadena.find("alto") is not -1:
                    nivel_oferta = 5
                if cadena.find("medio") is not -1:
                    nivel_oferta = 3
                if cadena.find("bajo") is not -1:
                    nivel_oferta = 1
                if cadena.find("c2") is not -1:
                    nivel_oferta = 6
                if cadena.find("c1") is not -1:
                    nivel_oferta = 5
                if cadena.find("b2") is not -1:
                    nivel_oferta = 4
                if cadena.find("b1") is not -1:
                    nivel_oferta = 3
                if cadena.find("a2") is not -1:
                    nivel_oferta = 2
                if cadena.find("a1") is not -1:
                    nivel_oferta = 1
                if nivel_oferta <= nivel_user:
                    return True
                else:
                    return False
        return True

#sería interesante primero filtrar por la titulación
#luego filtrar por los requesitos mínimos
def __comprueba_imprescindible(users, oferta):
    nota = 0
    if oferta.get("imprescindible") is not None:
        imprescindible = oferta.get("imprescindible").lower()
        for desarrollo in users.get("desarrollo"):
            for key in desarrollo:
                if key.lower() in imprescindible:
                    nota += int(desarrollo[key])
    return nota

def __filtra_ofertas(users):
    ofertas = mongoClient.ofertas
    collection_offer = ofertas.ofertas
    cursor_offer = collection_offer.find()
    ofertas = []
    #primero compruebo desplazamiento
    for offers in cursor_offer:
        if __comprueba_desplazamiento(users, offers) is not None:
            ofertas.append(__comprueba_desplazamiento(users, offers))
    #segundo idiomas
    if ofertas is not None:
        for offers in ofertas:
            if __comprueba_idiomas(users, offers, "imprescindible", "ingl", 'ingles') is False:
                ofertas.remove(offers)
            if __comprueba_idiomas(users, offers, "requisitos", "ingl", 'ingles') is False:
                ofertas.remove(offers)
            if __comprueba_idiomas(users, offers, "imprescindible", "franc", 'frances') is False:
                ofertas.remove(offers)
            if __comprueba_idiomas(users, offers, "requisitos", "franc", 'frances') is False:
                ofertas.remove(offers)
            if __comprueba_idiomas(users, offers, "imprescindible", "alem", 'aleman') is False:
                ofertas.remove(offers)
            if __comprueba_idiomas(users, offers, "requisitos", "alem", 'aleman') is False:
                ofertas.remove(offers)
    #tercero titulacion
    #if ofertas is not None:

    #cuarto compruebo requisitos mínimos
    if ofertas is not None:
        for offers in ofertas:
            offers['nota_user'] = __comprueba_imprescindible(users, offers)
    return ofertas