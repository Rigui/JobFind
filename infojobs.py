# -*- coding: utf-8 -*-
import requests
import oferta_class
from nltk.stem.porter import *
from nltk.tokenize import *
import Obtener_ofertas


def __tokenization_and_stemmer(line):
    tokenized_words = [PorterStemmer().stem(word) for word in word_tokenize(line.lower().decode('utf-8'), 'spanish')]
    return tokenized_words


def get_infojobs(competencias_bd, imprescindible_bd):

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
            nivel_titulacion = Obtener_ofertas.__get_nivel_titulacion(str(titulacion), nivel_titulacion)
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
            requirement_min = offer["requirementMin"].encode('utf-8')
            # requirements = [line for line in requirement_min.split("\n")]
            requisitos_prev = [word for word in word_tokenize(requirement_min.lower().decode('utf-8'), 'spanish')]
            competencias = []
            imprescindible = []
            # for req in requisitos_prev:
            #     if req in competencias_bd and req not in competencias:
            #         competencias.append(req)
            #     if req in imprescindible_bd and req not in imprescindible:
            #         imprescindible.append(req)

            for compet in competencias_bd:
                if compet.split(" ").__len__() > 1:
                    compet_split = compet.split(" ")
                    split_len = len(compet_split)
                    if compet_split[0] in requisitos_prev:
                        indexes = [n for (n, e) in enumerate(requisitos_prev) if e == compet_split[0]]
                        for index in indexes:
                            all_compet = True
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
                    if compet_split[0] in requisitos_prev:
                        indexes = [n for (n, e) in enumerate(requisitos_prev) if e == compet_split[0]]
                        for index in indexes:
                            all_compet = True
                            for i in xrange(1, split_len):
                                if compet_split[i] is not requisitos_prev[index + i]:
                                    all_compet = False
                            if all_compet and impresc not in imprescindible:
                                imprescindible.append(impresc)
                elif impresc in requisitos_prev and impresc not in imprescindible:
                    imprescindible.append(impresc)

            oferta = oferta_class.Oferta(link, city, job_title, published_date, author_name)
            oferta.nivel_titulacion = nivel_titulacion
            oferta.categoria = category
            oferta.subcategoria = subcategory
            oferta.salario_min = salary_min
            oferta.provincia = province
            oferta.requisitos = requirement_min
            oferta.experiencia_min = experience
            oferta.imprescindible = imprescindible
            oferta.competencias = competencias
            ofertas.append(oferta.to_json())

        return ofertas

