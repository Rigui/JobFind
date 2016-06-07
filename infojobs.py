# -*- coding: utf-8 -*-
import requests
import oferta_class
from nltk.stem.porter import *
from nltk.tokenize import *


def __tokenization_and_stemmer(line):
    tokenized_words = [PorterStemmer().stem(word) for word in word_tokenize(line.lower().decode('utf-8'), 'spanish')]
    return tokenized_words


def get_infojobs():

    req = requests.get('https://api.infojobs.net/api/1/offer',
                       auth=('2fe25988a01f48c59b36425abd6329b8', 'DHn5nyC8m1ByxAT1tnJUHjmwr4oZuYV82vVKlXqOKdCh6h4E05'))

    if req.status_code is 200:
        res_json = req.json()
        ofertas = []
        for offer in res_json["offers"]:
            province = str(offer["province"]["value"].encode('utf-8')).lower()
            city = str(offer["city"].lower().encode('utf-8'))
            published_date = __tokenization_and_stemmer(offer["published"].encode('utf-8'))
            link = offer["link"]
            updated_date = __tokenization_and_stemmer(offer["updated"].encode('utf-8'))
            job_title = __tokenization_and_stemmer(offer["title"].encode('utf-8'))
            titulacion = offer["study"]["value"].encode('utf-8')
            nivel_titulacion = 0
            nivel_titulacion = __get_nivel_titulacion(str(titulacion), nivel_titulacion)
            titulacion = __tokenization_and_stemmer(titulacion)
            author_name = offer["author"]["name"]
            author_uri = __tokenization_and_stemmer(offer["author"]["uri"].encode('utf-8'))
            experience = __tokenization_and_stemmer(offer["experienceMin"]["value"].encode('utf-8'))
            salary_max = __tokenization_and_stemmer(offer["salaryMax"]["value"].encode('utf-8'))
            salary_min = __tokenization_and_stemmer(offer["salaryMin"]["value"].encode('utf-8'))
            category = __tokenization_and_stemmer(offer["category"]["value"].encode('utf-8'))
            subcategory = __tokenization_and_stemmer(offer["subcategory"]["value"].encode('utf-8'))
            contract_type = __tokenization_and_stemmer(offer["contractType"]["value"].encode('utf-8'))
            urgent = offer["urgent"]
            work_day = __tokenization_and_stemmer(offer["workDay"]["value"].encode('utf-8'))
            salary_period = __tokenization_and_stemmer(offer["salaryPeriod"]["value"].encode('utf-8'))
            requirement_min = __tokenization_and_stemmer(offer["requirementMin"].encode('utf-8'))
            # requirements = [line for line in requirement_min.split("\n")]

            oferta = oferta_class.Oferta(link, city, job_title, published_date, author_name)
            oferta.nivel_titulacion = nivel_titulacion
            oferta.categoria = category
            oferta.subcategoria = subcategory
            oferta.salario_min = salary_min
            oferta.provincia = province
            oferta.requisitos = requirement_min
            oferta.experiencia_min = experience
            ofertas.append(oferta.to_json())

        return ofertas


def __get_nivel_titulacion(txt, nivel_titulacion):
    if "doct" in txt.lower() and (nivel_titulacion > 6 or nivel_titulacion is 0):
        nivel_titulacion = 6
    if "licenciado" in txt.lower() or "máster" in txt.lower() \
            or ("enxeñeiro" in txt.lower() and "técnico" not in txt.lower()) \
            and (nivel_titulacion > 5 or nivel_titulacion is 0):
        nivel_titulacion = 5
    if "diplomado" in txt.lower() or "grao" in txt.lower() \
            or "enxeñeiro técnico" in txt.lower() and (nivel_titulacion > 4 or nivel_titulacion is 0):
        nivel_titulacion = 4
    if "ciclo" in txt.lower() and (nivel_titulacion > 3 or nivel_titulacion is 0):
        nivel_titulacion = 3
    if "bacharelato" in txt.lower() and (nivel_titulacion > 2 or nivel_titulacion is 0):
        nivel_titulacion = 2
    if "secundaria" in txt.lower() and (nivel_titulacion > 1 or nivel_titulacion is 0):
        nivel_titulacion = 1
    return nivel_titulacion