# -*- coding: utf-8 -*-
import time
import webbrowser

import requests
from bs4 import BeautifulSoup
from linkedin import LinkedIn, LinkedInApi
from nltk.stem.porter import *
from nltk.tokenize import *

import Users
import mongodb

database_ip = "52.208.8.144"
database_port = 8080
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


def __get_public_profile(li, access_token):
    liapi = LinkedInApi(li)
    response = liapi.doApiRequest("https://api.linkedin.com/v1/people/~:(public-profile-url)", access_token)
    soup = BeautifulSoup(response)
    public_url = soup.find('public-profile-url').string
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    return requests.request('GET', public_url, headers=headers)


def __get_skills_linkedin(li, access_token, habilidadesDB, competenciasDB):
    habilidades_dict = {}
    competencias_dict = {}
    req = __get_public_profile(li, access_token)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text)
        for div in html.find_all('li', {'class': 'skill'}):
            skills = div.find_all('a')
            for skill in skills:
                conocimiento = skill.get('title').lower()
                if conocimiento in competenciasDB:
                    competencias_dict[conocimiento] = 2
                elif conocimiento in habilidadesDB:
                    habilidades_dict[conocimiento] = 2
                else:
                    habilidades_dict[conocimiento] = 2
                    habilidadesDB.append(conocimiento)
    return habilidades_dict, competencias_dict, habilidadesDB, competenciasDB


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
    nivel_titulacion_maximo = 0
    req = __get_public_profile(li, access_token)
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
            nivel_titulacion, titulacion = __inferir_nivel_titulo(nombre_titulo)
            if nivel_titulacion > nivel_titulacion_maximo:
                nivel_titulacion_maximo = nivel_titulacion
            estudios_list.append([titulacion, nombre_titulo, nombre_centro, fecha_inicio, fecha_fin])
    return estudios_list, nivel_titulacion_maximo


def __get_idiomas(li, access_token):
    idiomas_dic = {}
    req = __get_public_profile(li, access_token)
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
    localidad = soup.find('name').string.split()
    return localidad[0]


def __get_empresas(li, access_token, habilidades_dict, habilidadesDB):
    req = __get_public_profile(li, access_token)
    status_code = req.status_code
    if status_code == 200:
        fecha_inicio = fecha_fin = 0
        empresas = []
        html = BeautifulSoup(req.text)
        for div in html.find_all('li', {'class': 'position'}):
            nombre_empresa = div.find_all('h5', {'class': 'item-subtitle'})[0].getText().lower()
            fechas = div.find_all('time')
            index = 0
            for fecha in fechas:
                if index == 0:
                    fecha = fecha.getText().split()
                    fecha_inicio = fecha[len(fecha) - 1].lower()
                else:
                    fecha = fecha.getText().split()
                    fecha_fin = fecha[len(fecha) - 1].lower()
                    if "actu" in fecha_fin:
                        fecha_fin = time.strftime("%Y")
                index += 1
            anos = int(fecha_fin) - int(fecha_inicio)
            # Inferir conocimientos
            descripcion = div.find_all('p', {'class': 'description'})
            descripcion_token = descripcion[0].getText().lower().split()
            funciones = []
            for palabra in descripcion_token:
                if palabra in habilidadesDB:
                    funciones.append(palabra)
                    habilidades_dict[palabra] = 3
            empresas.append([nombre_empresa, funciones, fecha_inicio, fecha_fin, anos])
    return empresas, habilidades_dict


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
    nivel_idioma = 1
    txt = txt.lower().split()
    if "native" in txt:
        nivel_idioma = 6
    if "full" in txt:
        nivel_idioma = 5
    if "working" in txt:
        nivel_idioma = 4
    if "limited" in txt:
        nivel_idioma = 3
    if "elementary" in txt:
        nivel_idioma = 2
    return nivel_idioma


def __inferir_nivel_titulo(txt):
    nivel_titulacion = 0
    titulacion = ""
    txt = txt.lower().split()
    if "doct" in txt:
        nivel_titulacion = 6
        titulacion = "doct"
    if "licenciado" in txt or "máster" in txt or "master" in txt:
        nivel_titulacion = 5
        titulacion = "licenciado"
    if "diplomado" in txt or "grao" in txt or "enxeñeiro técnico" in txt or "grado" in txt or "graduado" in txt:
        nivel_titulacion = 4
        titulacion = "diplomado"
    if "ciclo" in txt:
        nivel_titulacion = 3
        titulacion = "ciclo"
    if "bacharelato" in txt or "bachillerato" in txt:
        nivel_titulacion = 2
        titulacion = "bachillerato"
    if "secundaria" in txt:
        nivel_titulacion = 1
        titulacion = "secundaria"
    return nivel_titulacion, titulacion


def __tokenization_and_stemmer(line):
    tokenized_words = [PorterStemmer().stem(word) for word in word_tokenize(line.lower().decode('utf-8'), 'spanish')]
    return tokenized_words


def __get_requisitos(db_requisitos):
    habilidadesDB = []
    competenciasDB = []
    imprescindibles = mongodb.get_element(db_requisitos, {'nivReq': 'imprescindible'})
    competencias = mongodb.get_element(db_requisitos, {'nivReq': 'competencias'})
    for imprescindible_values in imprescindibles:
        for skill in imprescindible_values['value']:
            habilidadesDB.append(skill)
    for competencias_values in competencias:
        for skill in competencias_values['value']:
            competenciasDB.append(skill)
    return habilidadesDB, competenciasDB


# def user_actualizacion_skills():
def get_linkedin_info():
    db_requisitos = mongodb.get_db(database_ip, database_port, database_requisitos)
    habilidadesDB, competenciasDB = __get_requisitos(db_requisitos)
    linkedin_conection, access_token = __conect_to_linkedin()
    print "Conectado al perfil de linkedin\n Obteniendo datos"
    nombre, apellidos = __get_nombre(linkedin_conection, access_token)
    ciudad = __get_localidad(linkedin_conection, access_token)
    habilidades_dict, competencias_dict, habilidadesDB, competenciasDB = __get_skills_linkedin(linkedin_conection,
                                                                                               access_token,
                                                                                               habilidadesDB,
                                                                                               competenciasDB)
    empresas, habilidades_dict = __get_empresas(linkedin_conection, access_token, habilidades_dict, habilidadesDB)
    email = __get_email(linkedin_conection, access_token)
    idiomas = __get_idiomas(linkedin_conection, access_token)
    estudios_dict, nivel_titulacion = __get_estudios(linkedin_conection, access_token)
    # creamos la entidad usuario
    print "Datos Obtenidos\nGuardando..."
    db_user = mongodb.get_db(database_ip, database_port, database_usuarios)

    usuario_db = db_user.find_one({'email': email})
    usuario = None
    if usuario_db is not None:
        print "Usuario encontrado\nActualizando..."
        usuario = Users.Users(nombre, apellidos)
        usuario.id = usuario_db['_id']
        usuario.ciudad = usuario_db['ciudad']
        usuario.idiomas = usuario_db['idiomas']
        usuario.nivel_titulacion = usuario_db['nivel_titulacion']
        usuario.competencias = usuario_db['competencias']
        usuario.habilidades = usuario_db['habilidades']
        usuario.estudios = usuario_db['estudios']
        usuario.empresas = usuario_db['empresas']
    else:
        usuario = Users.Users(nombre, apellidos)

    usuario.ciudad = ciudad
    usuario.email = email
    usuario.idiomas = idiomas
    usuario.nivel_titulacion = nivel_titulacion
    if usuario.competencias is None:
        usuario.competencias = competencias_dict
    else:
        usuario.competencias.update(competencias_dict)
    if usuario.habilidades is None:
        usuario.habilidades = habilidades_dict
    else:
        usuario.habilidades.update(habilidades_dict)
    if usuario.estudios is None:
        usuario.estudios = estudios_dict
    else:
        for estudio in estudios_dict:
            if estudio not in usuario.estudios:
                usuario.estudios.append(estudio)
    if usuario.empresas is None:
        usuario.empresas = empresas
    else:
        for empresa in empresas:
            if empresa not in usuario.empresas:
                usuario.empresas.append(empresa)
    mongodb.add_update_element(db_user, usuario.toDBCollection())
    print "Usuario Guardado: " + nombre + " " + apellidos
    return
