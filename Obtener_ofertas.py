# -*- coding: utf-8 -*-
import scrapping_uvigo
import infojobs
import mongodb

database_ip = "52.208.8.144"
database_port = 8080
database_ofertas = "ofertas"
database_requisitos = "requisitos"


def obtener_ofertas():
    print "Obtener base de datos"
    ofertas_db = mongodb.get_db(database_ip, database_port, database_ofertas)
    requisitos_db = mongodb.get_db(database_ip, database_port, database_requisitos)
    imprescindible_elements = mongodb.get_element(requisitos_db, {"nivReq": "imprescindible"})
    competencias_elements = mongodb.get_element(requisitos_db, {"nivReq": "competencias"})

    competencias = []
    for compet in competencias_elements:
        for values in compet['value']:
            competencias.append(values)

    imprescindible = []
    for impresc in imprescindible_elements:
        for values in impresc['value']:
            imprescindible.append(values)

    print "Obtener ofertas de Uvigo"
    ofertas_uvigo = scrapping_uvigo.get_uvigo(competencias, imprescindible)
    for oferta_uvigo in ofertas_uvigo:
        mongodb.add_update_element(ofertas_db, oferta_uvigo)

    print "Obtener ofertas de Infojobs"
    ofertas_infojobs = infojobs.get_infojobs(competencias, imprescindible)
    for each_oferta in ofertas_infojobs:
        mongodb.add_update_element(ofertas_db, each_oferta)

    return


def __get_nivel_titulacion(txt, nivel_titulacion):
    if "doct" in txt.lower() and (nivel_titulacion > 6 or nivel_titulacion is 0):
        nivel_titulacion = 6
    if "licenciado" in txt.lower() or "máster" in txt.lower() \
            or (("enxeñeiro" in txt.lower() or "ingeniero") and "técnico" not in txt.lower()) \
            and (nivel_titulacion > 5 or nivel_titulacion is 0):
        nivel_titulacion = 5
    if "diplomado" in txt.lower() or "grao" in txt.lower() \
            or "enxeñeiro técnico" in txt.lower() and (nivel_titulacion > 4 or nivel_titulacion is 0):
        nivel_titulacion = 4
    if "ciclo" in txt.lower() and (nivel_titulacion > 3 or nivel_titulacion is 0):
        nivel_titulacion = 3
    if ("bacharelato" in txt.lower() or "bachiller" in txt.lower()) and (nivel_titulacion > 2 or nivel_titulacion is 0):
        nivel_titulacion = 2
    if "secundaria" in txt.lower() and (nivel_titulacion > 1 or nivel_titulacion is 0):
        nivel_titulacion = 1
    return nivel_titulacion
