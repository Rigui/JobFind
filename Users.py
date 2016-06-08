# -*- coding: utf-8 -*-

class Users:
    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        self.pais = None
        self.comunidad = None
        self.provincia = None
        self.ciudad = None
        self.estudios = None #[[Titulacion,Nombre titulacion, fecha inicio, fecha fin],]
        self.nivel_titulacion = None
        self.idiomas = None  # {{idioma:nivel}}
        self.empresas = None  # [[Nombre empresa, funciones, fecha inicio, fecha fin, años],]
        self.remuneracion = None
        self.desplazamiento = None
        self.competencias = None  # {{competencia:nivel},}
        self.habilidades = None  # {{competencia:nivel},}
        self.email = None
        self._id = None

    def toDBCollection(self):
        return {
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "pais": self.pais,
            "comunidad": self.comunidad,
            "provincia": self.provincia,
            "ciudad": self.ciudad,
            "estudios": self.estudios,
            "nivel_titulacion": self.nivel_titulacion,
            "idiomas": self.idiomas,
            "empresas": self.empresas,
            "remuneracion": self.remuneracion,
            "desplazamiento": self.desplazamiento,
            "competencias": self.competencias,
            "habilidades": self.habilidades,
            "email": self.email,
            '_id': self._id,
        }

    def __str__(self):
        return "Nombre: %s - Apellidos: %s - Provincia: %s - Localidad: %s" % (
            self.nombre, self.apellidos, self.provincia, self.ciudad)
