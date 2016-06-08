# -*- coding: utf-8 -*-
from geopy.distance import vincenty
from geopy.exc import GeocoderServiceError
from geopy.geocoders import GeoNames
from geopy.geocoders import Nominatim

geolocator = Nominatim()
geonames = GeoNames(username="demo")


def calculo_distancia_ciudades(ciudad_usuario, ciudad_oferta):
    location_user = get_location_ciudad(ciudad_usuario)
    location_oferta = get_location_ciudad(ciudad_oferta)
    usuario_cordenadas = (location_user.latitude, location_user.longitude)
    oferta_cordenadas = (location_oferta.latitude, location_oferta.longitude)
    return vincenty(usuario_cordenadas, oferta_cordenadas).kilometers


def get_provincia(ciudad):
    localizacion = get_ciudad_completa(ciudad)
    if localizacion is None:
        provincia = None
    else:
        localizacion = localizacion.split(",")
        longitud = localizacion.__len__()
        if longitud >= 5:
            provincia = localizacion[2]
        elif longitud is 4:
            provincia = localizacion[1]
        else:
            provincia = localizacion[0]
    return provincia


def get_comunidad(ciudad):
    localizacion = get_ciudad_completa(ciudad)
    if localizacion is None:
        comunidad = None
    else:
        localizacion = localizacion.split(",")
        longitud = localizacion.__len__()
        if longitud >= 5:
            comunidad = localizacion[3]
        elif longitud is 4:
            comunidad = localizacion[2]
        elif longitud is 1:
            comunidad = localizacion[0]
        else:
            comunidad = localizacion[1]
    return comunidad


def get_pais(ciudad):
    localizacion = get_ciudad_completa(ciudad)
    if localizacion is None:
        pais = None
    else:
        localizacion = localizacion.split(",")
        longitud = localizacion.__len__()
        if longitud >= 5:
            pais = localizacion[4]
        elif longitud is 4:
            pais = localizacion[3]
        elif longitud is 2:
            pais = localizacion[1]
        elif longitud is 1:
            pais = localizacion[0]
        else:
            pais = localizacion[2]
    return pais


def get_ciudad_completa(ciudad):
    location = get_location_ciudad(ciudad)
    if location is None:
        return None
    return location.address.lower()


def get_location_ciudad(ciudad):
    try:
        cordenadas = geonames.geocode(ciudad)
        if cordenadas is not None:
            ciudad_correcta = cordenadas.address.split(",")[0]
        else:
            ciudad_correcta =ciudad
    except GeocoderServiceError:
        ciudad_correcta = ciudad
    location = geolocator.geocode(ciudad_correcta)
    if location is None:
        return None
    return location
