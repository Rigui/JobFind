# -*- coding: utf-8 -*-
import webbrowser

import requests
from bs4 import BeautifulSoup
from linkedin import LinkedIn, LinkedInApi
from nltk.stem.porter import *
from nltk.tokenize import *

import Users

database_ip = "52.208.8.144"
database_port = 27017
database_requisitos = "requisitos"
database_ofertas = "ofertas"
database_usuarios = "Users"
__API_KEY = "776iq1i9wuca2b"
__SECRET_KEY = "GYasmOX4Zgcjn9N2"


def __conect_to_linkedin():
    li = LinkedIn(__API_KEY, __SECRET_KEY)
    token = li.getRequestToken(None)
    # prompt user in the web browser to login to LinkedIn and then enter a code that LinkedIn gives to the user
    auth_url = li.getAuthorizeUrl(token)
    webbrowser.open(auth_url)
    validator = input("Enter token: ")
    access_token = li.getAccessToken(token, validator)
    return li, access_token

def __get_public_profile(li,access_token):
    liapi = LinkedInApi(li)
    response = liapi.doApiRequest("https://api.linkedin.com/v1/people/~:(public-profile-url)", access_token)
    soup = BeautifulSoup(response)
    public_url = soup.find('public-profile-url').string
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    return requests.request('GET', public_url, headers=headers)

def __get_skills_linkedin(li, access_token):
    skills_list = []
    req = __get_public_profile(li,access_token)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text)
        for div in html.find_all('li', {'class': 'skill'}):
            skills = div.find_all('a')
            for skill in skills:
                skills_list.append(skill.get('title').lower())
    return skills_list


def __get_email(li, access_token):
    liapi = LinkedInApi(li)
    response = liapi.doApiRequest("https://api.linkedin.com/v1/people/~:(email-address)", access_token)
    soup = BeautifulSoup(response)
    email = soup.find('email-address').string
    return email


def __get_nombre(li, access_token):
    liapi = LinkedInApi(li)
    response = liapi.doApiRequest("https://api.linkedin.com/v1/people/~", access_token)
    soup = BeautifulSoup(response)
    name = soup.find('first-name').string
    apellidos = soup.find('last-name').string
    return name, apellidos


def __get_estudios(li, access_token):
    estudios_list = []
    req = __get_public_profile(li,access_token)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text)
        for div in html.find_all('li', {'class': 'school'}):
            nombre_titulo = nombre_centro = fecha_fin = fecha_inicio = None
            studios = div.find_all('h5', {'class': 'item-subtitle'})
            for estudio in studios:
                estudio_name = estudio.find_all('span', {'class': 'translation'})
                for name in estudio_name:
                    nombre_titulo = name.getText().lower()

            centros = div.find_all('h4', {'class': 'item-title'})
            for centro in centros:
                centro_names = centro.find_all('span', {'class': 'translation'})
                for name in centro_names:
                    nombre_centro = name.getText().lower()

            fechas = div.find_all('time')
            index = 0
            for fecha in fechas:
                if index == 0:
                    fecha_inicio = fecha.getText().lower()
                else:
                    fecha_fin = fecha.getText().lower()
                index += 1
            estudios_list.append(['nivel titulo', nombre_titulo, nombre_centro, fecha_inicio, fecha_fin])
    return estudios_list

def __get_idiomas(li, access_token):
    idiomas_dic = {}
    req = __get_public_profile(li,access_token)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text)
        for div in html.find_all('li', {'class': 'language'}):
            idioma = div.find_all('h4', {'class': 'name'})[0].getText().lower()
            nivel = div.find_all('p', {'class': 'proficiency'})[0].getText().lower()
            idiomas_dic[idioma] = __inferir_nivel_idioma(nivel)
    return idiomas_dic


def __get_localidad(li, access_token):
    liapi = LinkedInApi(li)
    response = liapi.doApiRequest("https://api.linkedin.com/v1/people/~:(location)", access_token)
    soup = BeautifulSoup(response)
    localidad = soup.find('name').string
    return localidad


def __get_experiencia_inferir_skills(li, access_token, db_requisitos):
    new_competencias = []
    new_imprescindibles = []
    # TODO Substituir por db
    competencias = ["adaptabilidad", "iniciativa", "trabajo en equipo", "decisión", "gestión", "xestión",
                    "organización", "planificación", "aprendizaje autónomo", "creatividad", "resolución",
                    "responsabilidad", "comunicación", "líder", "calidad", "ganas", "motivación", "identificación",
                    "voluntariado"]
    imprescindible = ["ofimática", "word", "excel", "autómatas", "java", "html5", "javaee", "relacionales",
                      "arquitectura de sistemas", "e-commerce", "pyme", "internet", "redes sociales", "vehículo",
                      "conducir", "linux", "http", "tcp/ip", "c++", "c#", "javascript", "ajax", "interfaz",
                      "modelado 3d", "grandes volúmenes de datos", "git", "autocad", "contabilidad", "diseño",
                      "software", "nube", "web", "móvil", "móbil", "gestión de obra", "alimentos", "derecho",
                      "autoempleo", "informática", "igualdad de género"]

    req = __get_public_profile(li,access_token)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text)
        for div in html.find_all('li', {'class': 'position'}):
            descripcion = div.find_all('p', {'class': 'description'})
            descripcion_token = __tokenization_and_stemmer(descripcion[0].getText().lower())
            print descripcion_token
            for palabra in descripcion_token:
                '''if palabra.encode('utf-8') in competencias:
                    print palabra.encode('utf-8')'''
                if "relacionales" in competencias:
                    print "encontrado a mano"

    return new_competencias, new_imprescindibles


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

def __inferir_nivel_idioma(txt):
    nivel_idioma = 0
    if "nativa" in txt.lower():
        nivel_idioma = 5
    if "completa" in txt.lower() and "profesional" in txt.lower():
        nivel_idioma = 4
    if "sica" in txt.lower() and "profesional" in txt.lower():
        nivel_idioma = 3
    if "limitada" in txt.lower():
        nivel_idioma = 2
    if "basica" in txt.lower():
        nivel_idioma = 1
    return nivel_idioma


def __tokenization_and_stemmer(line):
    tokenized_words = [PorterStemmer().stem(word) for word in word_tokenize(line.lower().decode('utf-8'), 'spanish')]
    return tokenized_words


# def user_actualizacion_skills():
def get_linkedin_info():
    linkedin_conection, access_token = __conect_to_linkedin()
    nombre, apellidos = __get_nombre(linkedin_conection, access_token)
    localidad = __get_localidad(linkedin_conection, access_token)
    skill_list = __get_skills_linkedin(linkedin_conection, access_token)
    email = __get_email(linkedin_conection, access_token)
    idiomas = __get_idiomas(linkedin_conection,access_token)
    estudios = __get_estudios(linkedin_conection, access_token)
    #skill_inferidas = __get_experiencia_inferir_skills(linkedin_conection, access_token, database_requisitos)
    usuario = Users.Users(nombre=nombre,apellidos=apellidos,localidad=localidad,estudios=estudios,competencias=skill_list)


''''db_requisitos = mongodb.get_db(database_ip, database_port, database_requisitos)
skill_inferidas = __get_experiencia_inferir_skills(linkedin_conection,access_token,db_requisitos)
db_user = mongodb.get_db(database_ip, database_port, database_usuarios)'''
