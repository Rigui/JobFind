# -*- coding: utf-8 -*-

class Users:

    def __init__(self, nombre, apellidos, pais, comunidad, provincia, ciudad, estudios, nivel_titulacion, idiomas, empresas, cursillos, remuneracion, desplazamiento, clase_contrato, competencias, desarrollo, sistemas):
        self.nombre = nombre
        self.apellidos = apellidos
        self.pais = pais
        self.comunidad = comunidad
        self.provincia = provincia
        self.ciudad = ciudad
        self.estudios = estudios
        self.nivel_titulacion = nivel_titulacion
        self.idiomas = idiomas
        self.empresas = empresas
        self.cursillos = cursillos
        self.remuneracion = remuneracion
        self.desplazamiento = desplazamiento
        self.clase_contrato = clase_contrato
        self.competencias = competencias
        self.desarrollo = desarrollo
        self.sistemas = sistemas

    def toDBCollection (self):
        return{
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
