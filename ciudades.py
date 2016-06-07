# -*- coding: utf-8 -*-
from geopy.geocoders import Nominatim
from geopy.geocoders import GeoNames
from geopy.distance import vincenty

geolocator = Nominatim()
geonames = GeoNames(username="demo")

def calculo_distancia_ciudades(ciudad_usuario, ciudad_oferta):
    location_user = geolocator.geocode(ciudad_usuario)
    location_oferta = geolocator.geocode(ciudad_oferta)
    usuario_cordenadas = (location_user.latitude, location_user.longitude)
    oferta_cordenadas = (location_oferta.latitude, location_oferta.longitude)
    return vincenty(usuario_cordenadas, oferta_cordenadas).kilometers

def get_provincia(ciudad):
    localizacion = get_ciudad_completa(ciudad)
    if localizacion is None:
        provincia= None
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
        else:
            pais = localizacion[2]
    return pais

def get_ciudad_completa(ciudad):
    cordenadas = geonames.geocode(ciudad)
    if cordenadas is not None:
        ciudad_correcta = cordenadas.address.split(",")[0]
        location = geolocator.geocode(ciudad_correcta)
        if location is None:
            return None
    else:
        return None
    return location.address.lower()



def main():
    print(get_provincia({'city':"A Coruña"}))
    print(get_comunidad({'city':"A Coruña"}))
    print(get_pais({'city':"A Coruña"}))
    print(get_ciudad_completa("galicia"))
    print(calculo_distancia_ciudades("Vigo","pontevedra"))
    return

if __name__ == "__main__":
    main()



