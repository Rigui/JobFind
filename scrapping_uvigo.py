# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from nltk.stem.porter import *
from nltk.tokenize import *

import oferta_class

base_url = "http://emprego.uvigo.es/emprego_es/emprego/ofertas/"


def get_uvigo():
    links_ofertas = __links_ofertas_uvigo()
    ofertas = __scrapping_links(links_ofertas)
    return ofertas


def __tokenization_and_stemmer(line):
    tokenized_words = [PorterStemmer().stem(word) for word in word_tokenize(line.lower().decode('utf-8'), 'portuguese')]
    tokenized_words = tokenized_words.__str__()
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


def __scrapping_links(links):
    ofertas = []
    for url in links:
        req = requests.get(url)
        status_code = req.status_code
        if status_code == 200:
            html = BeautifulSoup(req.text, "lxml")  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            job_title = html.find('div', {'id': 'contido'}).find('h1').getText()
            city = fecha_inicio_publicacion = destinatarios = empresa = remuneracion = numero_vacantes = duracion = None
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
                    city = div.find_all('div')[1].getText()
                elif "Jornada completa".decode('utf-8') in div.getText():
                    jornada_completa = div.find_all('div')[1].getText()
                elif "Remuneración".decode('utf-8') in div.getText():
                    remuneracion = __tokenization_and_stemmer(div.find_all('div')[1].getText().encode('utf-8'))
                elif "Funciones".decode('utf-8') in div.getText():
                    funciones = div.find_all('div')[1].getText().encode('utf-8').replace("\nOFRÉCESE:\n", "")
                    if "Duración: " in funciones:
                        duracion = (str(funciones).split("Duración: ")[1]).split("\n")[0]
                        funciones = str(funciones).replace("Duración: "+duracion, "")
                elif "Conocimientos".decode('utf-8') in div.getText():
                    conocimientos = __tokenization_and_stemmer(div.find_all('div')[1].getText().encode('utf-8'))
                elif "Destinatarios".decode('utf-8') in div.getText():
                    destinatarios = __tokenization_and_stemmer(div.find_all('div')[1].getText().encode('utf-8'))
                elif "Empresa".decode('utf-8') in div.getText():
                    empresa = __tokenization_and_stemmer(div.find_all('div')[1].getText())

            oferta = oferta_class.Oferta(url, city, job_title, fecha_inicio_publicacion, empresa)
            oferta.salario_min = remuneracion
            oferta.numero_vacantes = numero_vacantes
            oferta.titulacion = destinatarios
            oferta.requisitos = funciones.decode('utf-8') + conocimientos
            if duracion is not None:
                oferta.duracion = duracion
            ofertas.append(oferta.to_json())

    return ofertas
