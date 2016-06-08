# -*- coding: utf-8 -*-
import Localidades
import mongodb

__database_ip = "52.208.8.144"
__database_port = 8080
__database_ofertas = "ofertas"
__database_usuarios = "Users"

def __actualizar_localizacion(database):
    for entrada_db in database.find():
        ciudad = entrada_db['ciudad'].split(" e ")
        indice = 0
        for city in ciudad:
            provincia = Localidades.get_provincia(city)
            comunidad = Localidades.get_comunidad(city)
            pais = Localidades.get_pais(city)
            if provincia is not None:
                if indice == 0:
                    entrada_db['provincia'] = provincia
                else:
                    entrada_db['provincia'] += ", " + provincia
            if comunidad is not None:
                if indice == 0:
                    entrada_db['comunidad'] = comunidad
                else:
                    entrada_db['comunidad'] += ", " + comunidad
            if pais is not None:
                if indice == 0:
                    entrada_db['pais'] = pais
                else:
                    entrada_db['pais'] += ", " + pais
            indice += 1
        mongodb.add_update_element(database, entrada_db)
    return


def actualizar_localizacion_ofertas():
    print "Actualizando localizaciones"
    __actualizar_localizacion(mongodb.get_db(__database_ip, __database_port, __database_ofertas))
    print "Localizaciones actualizadas"
    return


def actualizar_localizacion_usuarios():
    print "Actualizando localizaciones"
    __actualizar_localizacion(mongodb.get_db(__database_ip, __database_port, __database_usuarios))
    print "Localizaciones actualizadas"
    return


def __main():
    __actualizar_localizacion(mongodb.get_db(__database_ip, __database_port, __database_ofertas))
    # actualizar_localizacion(mongodb.get_db(database_ip, database_port, database_usuarios))
    return


if __name__ == "__main__":
    __main()
