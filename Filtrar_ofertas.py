# -*- coding: utf-8 -*-

from pymongo import *
import re
import Levenshtein

mongoClient = MongoClient('52.208.8.144', 8080)

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
        imprescindible = ""
        for campos in oferta.get(impres):
            imprescindible += campos
        imprescindible = imprescindible.lower()
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

def __comprueba_nivel_titulacion(users, oferta):
    if (int(users.get("nivel_titulacion")) >= int(oferta.get("nivel_titulacion"))):
        return True
    else:
        return False

def __comprueba_titulacion(users, oferta):
    if users.get("estudios") is not None:
        for titulo in users.get("estudios"):
            if oferta.get("titulacion") is not None:#uvigo
                for titulacion in oferta.get("titulacion"):
                    if Levenshtein.distance(titulo[1].rsplit(' ', 1)[1], titulacion) < 4:
                        return True
                return False
            return True
    elif oferta.get("titulacion") is None:
        return True
    else:
        return False

def __comprueba_exp_minima(users, oferta):
    years = 0
    for experiencia in oferta.get("experiencia_min"):
        year = re.findall('\d+', experiencia)
        if len(year) > 0:
            if years < year:
                years = year
    if years > 0:#se solicitan años de experiencia
        if users.get("empresas") is None:
            return False
        else:
            for empresas in users.get("empresas"):
                if empresas[-1] >= years:
                    return True
            return False
    else:
        return True

def __comprueba_requisitos(users, offers):
    for requisito in offers.get("imprescindible"):
        if requisito not in users.get("habilidades"):
            return False
        elif users.get("habilidades")[requisito] == 0:
            return False
    return True

def __filtra_ofertas(users):
    ofertas = mongoClient.ofertas
    collection_offer = ofertas.ofertas
    cursor_offer = collection_offer.find()
    ofertas = []

    #primero compruebo desplazamiento
    for offers in cursor_offer:
        if __comprueba_desplazamiento(users, offers) is not None:
            ofertas.append(__comprueba_desplazamiento(users, offers))
    print 'se han encontrado %i empresas' %(len(ofertas))
    #segundo idiomas
    if ofertas is not None:
        for offers in ofertas[:]:
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
    print 'se han quedado %i empresas después del tema de los idiomas' % (len(ofertas))
    #tercero nivel titulacion
    if ofertas is not None:
        for offers in ofertas[:]:
            if __comprueba_nivel_titulacion(users, offers) is False:
                ofertas.remove(offers)
    print 'se han quedado %i empresas después del tema del nivel de titulacion' % (len(ofertas))
    #cuarto titulacion
    if ofertas is not None:
        for offers in ofertas[:]:
            if __comprueba_titulacion(users, offers) is False:
                ofertas.remove(offers)
    print 'se han quedado %i empresas después del tema de la titulacion' % (len(ofertas))
    #quinto exp mínima
    if ofertas is not None:
        for offers in ofertas[:]:
            if offers.get("experiencia_min") is not None:
                if __comprueba_exp_minima(users, offers) is False:
                    ofertas.remove(offers)
    print 'se han quedado %i empresas después del tema de la exp mínima' % (len(ofertas))
    #sexto compruebo requisitos mínimos
    if ofertas is not None:
        for offers in ofertas[:]:
            if offers.get("imprescindible") is not None:
                if __comprueba_requisitos(users, offers) is False:
                    ofertas.remove(offers)
    print 'se han quedado %i empresas después del tema de los requisitos' % (len(ofertas))
    return ofertas