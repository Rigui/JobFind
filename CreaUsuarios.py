# -*- coding: utf-8 -*-

from pymongo import *
import Users

mongoClient = MongoClient('52.208.8.144', 8080)

db = mongoClient.Users

collection = db.Users

collection.remove()

user1 = Users.Users('Pablo', 'Domínguez Malleiro')
user2 = Users.Users('Rigui', 'Rigueira Cabrera')
user3 = Users.Users('Alex', 'Martín Merino')
user4 = Users.Users('Alberto', 'González Cristobo')
user5 = Users.Users('Barack', 'Obama')
user6 = Users.Users('Casius', 'Clay')
users = [
    user1, user2, user3, user4, user5, user6
]

user1.ciudad = "Madrid"
user2.ciudad = "Barcelona"
user3.ciudad = "Córdoba"
user4.ciudad = "Vigo"
user5.ciudad = "Madrid"
user6.ciudad = "Cangas"

user1.estudios = ["Bachiller", "", "Instituto ES Carballiño", "2000", "2004"]
user2.estudios = [["Doctor", "Doctorado en Ciencias del Mar", "Universidad de Vigo", "2013", "2016"], ["Máster", "Máster en Telecomunicaciones", "Univerdiadd de Vigo", "2009", "2013"]]
user3.estudios = ["Grado", "Graduado en Mecánica Cuántica", "Universidad de Massachusets", "2000", "2015"]
user4.estudios = [["Máster", "Máster en Filología Árabe", "2009", "2010"], ["Graduado", "Graduado en filología Inglesa", "2005", "2009"]]
user5.estudios = ["Ciclo", "Ciclo superior en Costura", "2005", "2009"]
user6.estudios = []

user1.nivel_titulacion = 2
user2.nivel_titulacion = 6
user3.nivel_titulacion = 4
user4.nivel_titulacion = 5
user5.nivel_titulacion = 3
user6.nivel_titulacion = 1

user1.desplazamiento = 0
user2.desplazamiento = 2
user3.desplazamiento = 0
user4.desplazamiento = 1
user5.desplazamiento = 3
user6.desplazamiento = 1

user1.habilidades = {'java': 1, 'word': 2, 'excel': 3, 'iniciativa': 2, 'windows': 3, 'presencia': 2, 'responsabilidad': 1}
user2.habilidades = {'ofimática': 1, 'conducir': 2, 'vehículo': 3, 'iniciativa': 2, 'windows': 3}
user3.habilidades = {'autómatas': 1, 'word': 2, 'excel': 3, 'iniciativa': 2, 'windows': 3}
user4.habilidades = {'html5': 1, 'java': 2, 'javaee': 3, 'e-commerce': 2, 'windows': 3}
user5.habilidades = {'software': 1, 'informática': 2, 'linux': 3, 'http': 2, 'javascript': 3, 'java': 3}
user6.habilidades = {'c': 1}

user1.competencias = {'adaptabilidad': 1, 'planificación': 2, 'responsabilidad': 3, 'iniciativa': 2, 'don de gentes': 3}
user2.competencias = {'iniciativa': 1, 'apredizaje autónomo': 2, 'comunicación': 3, 'iniciativa': 2, 'atención': 3}
user3.competencias = {'trabajo en equipo': 1, 'creatividad': 2, 'líder': 3, 'iniciativa': 2, 'presencia': 3}
user4.competencias = {'decisión': 1, 'moticación': 2, 'resolución': 3, 'liderazgo': 2, 'responsabilidad': 3}
user5.competencias = {'gestión': 1, 'identificación': 2, 'ganas': 3, 'calidad': 2, 'líder': 3, 'trabajo en equipo': 3}
user6.competencias = {'organización': 1}

user1.idiomas = {'ingles': 6, 'frances': 4}
user2.idiomas = {}
user3.idiomas = {'ingles': 2}
user4.idiomas = {}
user5.idiomas = {'ingles': 5}
user6.idiomas = {'ingles': 5}

for user in users:
    user.pais = "España"
    collection.insert(user.toDBCollection())