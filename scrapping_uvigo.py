# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from nltk.stem.porter import *
from nltk.tokenize import *
import Obtener_ofertas

import oferta_class

base_url = "http://emprego.uvigo.es/emprego_es/emprego/ofertas/"


def get_uvigo(competencias, imprescindible):
    links_ofertas = __links_ofertas_uvigo()
    ofertas = __scrapping_links(links_ofertas, competencias, imprescindible)
    return ofertas


def __tokenization_and_stemmer(line):
    tokenized_words = [PorterStemmer().stem(word) for word in word_tokenize(line.lower().decode('utf-8'), 'portuguese')]
    return tokenized_words


def __links_ofertas_uvigo():
    url = base_url + "index.html"
    req = requests.get(url)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "lxml")  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        contido = html.find(id='contido')  # Obtenemos todos los span donde estan los links
        all_links = contido.find_all('a')
        links = [base_url + entrada.get('href') for entrada in all_links if "resultado" in entrada.get('href')]
        return links
    else:
        return []


def __scrapping_links(links, competencias_bd, imprescindible_bd):
    ofertas = []
    for url in links:
        req = requests.get(url)
        status_code = req.status_code
        if status_code == 200:
            html = BeautifulSoup(req.text, "lxml")  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            job_title = __tokenization_and_stemmer(html.find('div', {'id': 'contido'}).find('h1').getText().encode('utf-8'))
            city = fecha_inicio_publicacion = destinatarios = empresa = remuneracion = numero_vacantes = duracion = None
            requirese = conocimientos = funciones = None
            nivel_titulacion = 0
            competencias = []
            imprescindible = []
            for div in html.find_all('div', {'class': 'taboa_fila'}):
                if "Tipo convocatoria" in div.getText():
                    tipo_convocatoria = div.find_all('div')[1].getText()
                elif "Número vacantes".decode('utf-8') in div.getText():
                    numero_vacantes = div.find_all('div')[1].getText()
                elif "Fecha Inicio Publicación".decode('utf-8') in div.getText():
                    fecha_inicio_publicacion = div.find_all('div')[1].getText()
                elif "Fecha Fin Publicación".decode('utf-8') in div.getText():
                    fecha_fin_publicacion = div.find_all('div')[1].getText()
                elif "Lugar de trabajo".decode('utf-8') in div.getText():
                    city = str(div.find_all('div')[1].getText().lower().encode('utf-8'))
                elif "Jornada completa".decode('utf-8') in div.getText():
                    jornada_completa = div.find_all('div')[1].getText()
                elif "Remuneración".decode('utf-8') in div.getText():
                    remuneracion = __tokenization_and_stemmer(div.find_all('div')[1].getText().encode('utf-8'))
                elif "Funciones".decode('utf-8') in div.getText():
                    funciones = div.find_all('div')[1].getText().encode('utf-8')
                    if "lugar de traballo" in funciones.lower():
                        city = str(funciones).lower().split("lugar de traballo: ")[1].split("\n")[0].lower()
                    # funciones = __tokenization_and_stemmer(funciones)
                elif "Conocimientos".decode('utf-8') in div.getText():
                    conocimientos = div.find_all('div')[1].getText().encode('utf-8')
                    # conocimientos = __tokenization_and_stemmer(conocimientos)
                elif "Destinatarios".decode('utf-8') in div.getText():
                    destinatarios = __tokenization_and_stemmer(div.find_all('div')[1].getText().encode('utf-8'))
                    titulaciones = str(destinatarios).split("|")
                    for titulo in titulaciones:
                        nivel_titulacion = Obtener_ofertas.__get_nivel_titulacion(titulo, nivel_titulacion)
                elif "Empresa".decode('utf-8') in div.getText():
                    empresa = div.find_all('div')[1].getText()

            if funciones is not None and conocimientos is not None:
                requisitos = funciones + conocimientos
            elif funciones is not None and conocimientos is None:
                requisitos = funciones
            else:
                requisitos = conocimientos

            requisitos_prev = [word for word in word_tokenize(requisitos.lower().decode('utf-8'), 'portuguese')]
            for compet in competencias_bd:
                if compet.split(" ").__len__() > 1:
                    compet_split = compet.split(" ")
                    split_len = len(compet_split)
                    all_compet = True
                    if compet_split[0] in requisitos_prev:
                        index = requisitos_prev.index(compet_split[0])
                        for i in xrange(1, split_len):
                            if compet_split[i] not in requisitos_prev[index + i]:
                                all_compet = False
                        if all_compet and compet not in competencias:
                            competencias.append(compet)
                elif compet in requisitos_prev and compet not in competencias:
                    competencias.append(compet)
            for impresc in imprescindible_bd:
                if impresc.split(" ").__len__() > 1:
                    compet_split = impresc.split(" ")
                    split_len = len(compet_split)
                    all_compet = False
                    if compet_split[0] in requisitos_prev:
                        index = requisitos_prev.index(compet_split[0])
                        all_compet = True
                        for i in xrange(1, split_len):
                            if compet_split[i] is not requisitos_prev[index + i]:
                                all_compet = False
                    if all_compet and impresc not in competencias:
                        competencias.append(impresc)
                elif impresc in requisitos_prev and impresc not in competencias:
                    competencias.append(impresc)

            # for req in requisitos_prev:
            #     if req in competencias_bd and req not in competencias:
            #         competencias.append(req)
            #     if req in imprescindible_bd and req not in imprescindible:
            #         imprescindible.append(req)

            oferta = oferta_class.Oferta(url, city, job_title, fecha_inicio_publicacion, empresa)
            oferta.salario_min = remuneracion
            oferta.numero_vacantes = numero_vacantes
            oferta.titulacion = destinatarios
            oferta.requisitos = requisitos
            oferta.imprescindible = imprescindible
            oferta.competencias = competencias
            oferta.requirese = requirese
            oferta.duracion = duracion
            oferta.nivel_titulacion = nivel_titulacion
            ofertas.append(oferta.to_json())

    return ofertas

