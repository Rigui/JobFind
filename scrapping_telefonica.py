# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import nltk

# base_url = "https://jobs.telefonica.com"
base_url = "http://emprego.uvigo.es/emprego_es/emprego/ofertas/"


def links_ofertas_telefonica():
    # url = base_url + "/search/?q=&locationsearch=spain"
    url = base_url + "index.html"
    req = requests.get(url)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "lxml")  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        # entradas = html.find_all('a', {'class': 'jobTitle-link'})  # Obtenemos todos los span donde estan los links
        contido = html.find('div', {'id': 'contido'})  # Obtenemos todos los span donde estan los links
        all_links = contido.find_all('a')
        # Recorremos todas las entradas para extraer los links
        # links = [base_url + entrada.get('href') for entrada in entradas if "search" not in entrada.get('href')]
        links = [base_url + entrada.get('href') for entrada in all_links if "resultado" in entrada.get('href')]
        return links
    else:
        return []


def scrapping_links(links):
    links = links[0:3]  # solo 3 resultados para probar y ver mas facilmente
    for url in links:
        print "-----------------------------------------------------------------------------------"
        print url
        req = requests.get(url)
        status_code = req.status_code
        if status_code == 200:
            print ""
            html = BeautifulSoup(req.text, "lxml")  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            contido = html.find('div', {'id': 'contido'})
            job_title = contido.find('h1')
            print job_title.getText()
            print ""
            all_divs = html.find_all('div', {'class': 'taboa_fila'})
            tipo_convotaria = numero_vacantes = fecha_inicio_publicacion = fecha_fin_publicacion = ""
            empresa = lugar_trabajo = jornada_completa = funciones = conocimientos = destinatarios = ""
            for div in all_divs:
                if "Tipo convocatoria" in div.getText():
                    tipo_convotaria = div.find_all('div')[1].getText()
                elif "Número vacantes".decode('utf-8') in div.getText():
                    numero_vacantes = div.find_all('div')[1].getText()
                elif "Fecha Inicio Publicación".decode('utf-8') in div.getText():
                    fecha_inicio_publicacion = div.find_all('div')[1].getText()
                elif "Fecha Fin Publicación".decode('utf-8') in div.getText():
                    fecha_fin_publicacion = div.find_all('div')[1].getText()
                elif "Empresa".decode('utf-8') in div.getText():
                    empresa = div.find_all('div')[1].getText()
                elif "Lugar de trabajo".decode('utf-8') in div.getText():
                    lugar_trabajo = div.find_all('div')[1].getText()
                elif "Jornada completa".decode('utf-8') in div.getText():
                    jornada_completa = div.find_all('div')[1].getText()
                elif "Funciones".decode('utf-8') in div.getText():
                    funciones = div.find_all('div')[1].getText()
                elif "Conocimientos".decode('utf-8') in div.getText():
                    conocimientos = div.find_all('div')[1].getText()
                elif "Destinatarios".decode('utf-8') in div.getText():
                    destinatarios = div.find_all('div')[1].getText()

            print tipo_convotaria
            print numero_vacantes
            print fecha_inicio_publicacion
            print fecha_fin_publicacion
            print empresa
            print lugar_trabajo
            print jornada_completa
            print funciones
            print conocimientos
            print destinatarios

            # job_title = html.find("h1", {"id": "job-title"}).getText()
            # date_posted = html.find("span", {"itemprop": "datePosted"}).getText().replace("\n", "")
            # job_location = html.find("span", {"itemprop": "jobLocation"}).getText()
            # print job_title
            # print "date_posted: {}".format(date_posted)
            # print "job_location: {}".format(job_location)
            #
            # span_description = html.find("span", {"itemprop": "description"})
            # # print span_description
            # if "jd" not in span_description.getText():
            #     print span_description

        else:
            return []


if __name__ == "__main__":
    links_ofertas = links_ofertas_telefonica()
    scrapping_links(links_ofertas)
