# -*- coding: utf-8 -*-

import os

import Localidades_update
import Obtener_ofertas
import linkedin_api
from enriquecimiento import enriquecimiento


def menu():
    """
    Función que limpia la pantalla y muestra nuevamente el menu
    """
    os.system('cls')  # NOTA para windows tienes que cambiar clear por cls
    print "Selecciona una opción"
    print "\t1 - Generar Base Datos ofertas"
    print "\t2 - Introducir usuario"
    print "\t3 - Busqueda ofertas"
    print "\t9 - Salir"


while True:
    # Mostramos el menu
    menu()

    # solicituamos una opción al usuario
    opcionMenu = raw_input("inserta un numero valor >> ")

    if opcionMenu == "1":
        print "Has pulsado la opción 1...\nGenerando Base Datos ofertas"
        Obtener_ofertas.obtener_ofertas()
        Localidades_update.actualizar_localizacion_ofertas()
        enriquecimiento()
    elif opcionMenu == "2":
        print "Has pulsado la opción 2...\n"
        linkedin = raw_input("¿Dispone de cuenta en linkedin? (s/n): ")
        if linkedin in 's':
            linkedin_api.get_linkedin_info()
        Localidades_update.actualizar_localizacion_usuarios()
    elif opcionMenu == "3":
        print ""
        print("Has pulsado la opción 3...\n")
        email = raw_input("Introduzca su email")
        print "Buscando ofertas que coincidan con tu perfil"
        # TODO busqueda
    elif opcionMenu == "9":
        print "Gracias"
        break
    else:
        print ""
        raw_input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
