# -*- coding: utf-8 -*-
import operator

from Users import *
from pymongo import *
import Filtrar_ofertas
import Relevancia
from operator import itemgetter
import oferta_class




# users = [
#     Users('Personaje1', 'Apellido1 Apellido1')#, 'España', 'madrid', 'Madrid', 'Madrid', [['graduado', 'Grado en Ingeniería de Tecnologías de Telecomunicación', 'Universidad de Vigo', '01/09/2010', '30/06/2014'], ['maestro', 'Máster en Ingeniería de Telecomunicación', 'Universidad de Vigo', '01/09/2014', '30/06/2016']], 4, {'frances': '5', 'ingles': '4'}, [], [], '2000', '1', 'practicas', [{'Adquisicion de conocimientos': '0'}, {'Analisis de problemas': '0'}, {'Aprendizaje autonomo': '0'}, {'Capacidad para gestionar la presion': '0'}, {'Creatividad e innovacion': '0'}, {'Gestion del cambio': '0'}, {'Iniciativa': '0'}, {'Liderazgo': '0'}, {'Negociacion': '0'}, {'Organizacion y planificacion': '0'}, {'Orientacion a resultados': '0'}, {'Planificacion': '0'}, {'Precision': '0'}, {'Rigor': '0'}, {'Solucionar problemas': '0'}, {'Toma de decisiones': '0'}, {'Trabajo en equipo': '0'}], [{'net': '0'}, {'Arquitectura': '0'}, {'ASP': '0'}, {'Autocad': '0'}, {'Creatividad e innovacion': '0'}, {'ORACLE': '0'}, {'SQL': '0'}, {'TOAD': '0'}, {'C#': '0'}, {'C': '0'}, {'C++': '0'}, {'COBOL': '0'}, {'AXAPTA': '0'}, {'MAXIMO': '0'}, {'ORACLE': '0'}, {'HTML': '2'}, {'HTML5': '3'}, {'Java': '0'}, {'Matlab': '0'}, {'PHP': '0'}, {'Automatas': '0'}, {'Python': '0'}, {'Remedy': '0'}, {'SAP': '0'}, {'Scada': '0'}, {'Sharepoint': '0'}, {'Siebel': '0'}, {'UML': '0'}, {'VHDL': '0'}, {'JavaEE': '0'}, {'SGBD': '0'}, {'e-commerce': '0'}, {'DB2': '0'}, {'Nav': '0'}], '3')
# ]

mongoClient = MongoClient('52.208.8.144', 8080)

db = mongoClient.Users

collection = db.Users

# collection.remove()

# for user in users:
#     collection.insert(user.toDBCollection())

cursor = collection.find()
#for user in cursor:
     #print "%s - %s - %s - %s - %s - %s" \
          #%(user['nombre'], user['apellidos'], user['provincia'], user['ciudad'], user['estudios'], user['idiomas'])

# ofertas = mongoClient.ofertas
#
# collection_offer = ofertas.ofertas
#
# cursor_offer = collection_offer.find()
#
# cursor = collection.find()

#for user in cursor:
    #for offers in cursor_offer:
        #if 'ingl' in offers.get("requisitos"):
            #if 'c2' in offers.get("requisitos").lower():
               # print offers.get("empresa")
                #print 'encontrado c2'
            #elif 'c1' in offers.get("requisitos").lower():
                #print offers.get("empresa")
                #print 'encontrado c1'
            #elif 'b2' in offers.get("requisitos").lower():
                #print offers.get("empresa")
                #print 'encontrado b2'
            #elif 'b1' in offers.get("requisitos").lower():
                #print offers.get("empresa")
                #print 'encontrado b1'

print 'hasta aquí'
# for user in cursor:
#     filtrar = Filtrar_ofertas.get_ofertas(user)
#     for filtro in filtrar:
#         print filtro

# for offer in Filtrar_ofertas.get_ofertas(cursor[0]):
#     print offer
# for offer1 in Filtrar_ofertas.get_ofertas(cursor[1]):
#     print offer1

ofertas = Relevancia.get_relevancia(cursor[1], Filtrar_ofertas.get_ofertas(cursor[1]))
ofertas = sorted(ofertas, key=operator.itemgetter("nota_user"), reverse=True)
for offers in ofertas:
    print offers.get("nota_user")
# for offer2 in  Filtrar_ofertas.get_ofertas(cursor[2]):
#     print offer2
# for offer3 in  Filtrar_ofertas.get_ofertas(cursor[3]):
#     print offer3
# for offer4 in  Filtrar_ofertas.get_ofertas(cursor[4]):
#     print offer4
# for offer5 in  Filtrar_ofertas.get_ofertas(cursor[5]):
#     print offer5

