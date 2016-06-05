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
            job_title = __tokenization_and_stemmer(html.find('div', {'id': 'contido'}).find('h1').getText())
            city = fecha_inicio_publicacion = destinatarios = empresa = remuneracion = numero_vacantes = duracion = None
            imprescindible = competencias = requirese = None
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
                    city = __tokenization_and_stemmer(div.find_all('div')[1].getText())
                elif "Jornada completa".decode('utf-8') in div.getText():
                    jornada_completa = div.find_all('div')[1].getText()
                elif "Remuneración".decode('utf-8') in div.getText():
                    remuneracion = __tokenization_and_stemmer(div.find_all('div')[1].getText().encode('utf-8'))
                elif "Funciones".decode('utf-8') in div.getText():
                    funciones = div.find_all('div')[1].getText().encode('utf-8')
                    if "REQ" in funciones and "RESE:" in funciones:
                        requirese = (str(funciones).lower().split("rese:")[1]).split("ofrécese")[0]
                        funciones = str(funciones).lower().replace(requirese, "")
                        requirese = __tokenization_and_stemmer(requirese)
                    if "Duración: " in funciones:
                        duracion = (str(funciones).lower().split("duración: ")[1]).split("\n")[0]
                        funciones = str(funciones).lower().replace("duración: " + duracion, "")
                        duracion = __tokenization_and_stemmer(duracion)
                    funciones = __tokenization_and_stemmer(funciones)
                elif "Conocimientos".decode('utf-8') in div.getText():
                    conocimientos = div.find_all('div')[1].getText().encode('utf-8')
                    if "imprescindible" in conocimientos.lower() and "competencias transversais" in conocimientos.lower():
                        print url
                        imprescindible = \
                            (str(conocimientos).lower().split("imprescindible")[1]).split("competencias transversais")[0]
                        competencias = str(conocimientos).lower().split("competencias transversais")[1]
                        conocimientos = str(conocimientos).lower().replace("imprescindible", "").replace(imprescindible, "")
                        conocimientos = str(conocimientos).lower().replace("competencias", "").replace(competencias, "")
                        imprescindible = __tokenization_and_stemmer(imprescindible)
                        competencias = __tokenization_and_stemmer(competencias)
                    elif "imprescindible" not in conocimientos.lower() and \
                                    "competencias transversais" in str(conocimientos).lower():
                        competencias = str(conocimientos).lower().split("competencias transversais")[1]
                        conocimientos = str(conocimientos).lower().replace(
                            "competencias transversais" + competencias, "")
                        competencias = __tokenization_and_stemmer(competencias)
                    conocimientos = __tokenization_and_stemmer(conocimientos)
                elif "Destinatarios".decode('utf-8') in div.getText():
                    destinatarios = __tokenization_and_stemmer(div.find_all('div')[1].getText().encode('utf-8'))
                elif "Empresa".decode('utf-8') in div.getText():
                    empresa = div.find_all('div')[1].getText()

            oferta = oferta_class.Oferta(url, city, job_title, fecha_inicio_publicacion, empresa)
            oferta.salario_min = remuneracion
            oferta.numero_vacantes = numero_vacantes
            oferta.titulacion = destinatarios
            oferta.requisitos = funciones.decode('utf-8') + conocimientos
            oferta.imprescindible = imprescindible
            oferta.competencias = competencias
            oferta.requirese = requirese
            oferta.duracion = duracion
            ofertas.append(oferta.to_json())

    return ofertas
