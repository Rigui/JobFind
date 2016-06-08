# -*- coding: iso-8859-15 -*-

import pymongo
from pymongo import *
import opBasicas


def generarExperiencia(col, doc):
    imprescindible = doc['imprescindible']
    competencias = doc['competencias']

    nivXP = (0.2 * 1/doc['nivel_titulacion'] + 0.8 * (0.75*valoracionRequisitos(len(imprescindible))) +
             0.25*valoracionRequisitos(len(competencias)))
    xp = int(nivXP)
    texto = ""
    if xp < 1:
        xpnew = int(nivXP * 12)
        texto += "Estimados " + str(xpnew) + u" meses de experiencia"
    elif xp == 1:
        texto += "Estimado " + str(xp) + u" año de experiencia"
    else:
        texto += "Estimados " + str(xp) + u" años de experiencia"
    doc["expMinima"] = texto
    col.save(doc)


def valoracionRequisitos(long):
    if long < 2:
        return 1
    elif 2 <= long < 4:
        return 2
    elif 4 <= long < 6:
        return 3
    elif 6 <= long < 8:
        return 4
    elif 6 <= long < 10:
        return 5
    elif 10 <= long < 12:
        return 6
    elif 12 <= long < 14:
        return 7
    elif 14 <= long < 16:
        return 8
    elif 16 <= long < 18:
        return 9
    else:
        return 10
