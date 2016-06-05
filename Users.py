# -*- coding: utf-8 -*-

class Users:

    def __init__(self, nombre, apellidos, provincia, localidad, estudios, empresas, cursillos, remuneracion, desplazmiento, clase_contrato, competencias, desarrollo, sistemas):
        self.nombre = nombre
        self.apellidos = apellidos
        self.provincia = provincia
        self.localidad = localidad
        self.estudios = estudios
        self.empresas = empresas
        self.cursillos = cursillos
        self.remuneracion = remuneracion
        self.desplazamiento = desplazmiento
        self.clase_contrato = clase_contrato
        self.competencias = competencias
        self.desarrollo = desarrollo
        self.sistemas = sistemas

    def toDBCollection (self):
        return{
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "provincia": self.provincia,
            "localidad": self.localidad,
            "estudios": self.estudios,
            "empresas": self.empresas,
            "cursillos": self.cursillos,
            "remuneracion": self.remuneracion,
            "desplazamiento": self.desplazamiento,
            "clase_contrato": self.clase_contrato,
            "competencias": self.competencias,
            "desarrollo": self.desarrollo,
            "sistemas": self.sistemas
        }

    def __str__(self):
        return "Nombre: %s - Apellidos: %s - Provincia: %s - Localidad: %s" %(self.nombre, self.apellidos, self.provincia, self.localidad)

