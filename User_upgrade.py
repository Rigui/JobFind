import json

import requests
import mongodb
import ciudades
from SPARQLWrapper import SPARQLWrapper, JSON

database_ip = "52.208.8.144"
database_port = 27017
database_ofertas = "ofertas"
database_usuarios = "Users"
database_habilidades = "skills"

def actualizar_localizacion(database):
    for entrada_db in database.find():
        ciudad = entrada_db['ciudad'].split(" e ")
        indice = 0
        for city in ciudad:
            provincia = ciudades.get_provincia(city)
            comunidad = ciudades.get_comunidad(city)
            pais = ciudades.get_pais(city)
            if provincia is not None:
                if indice == 0:
                    entrada_db['provincia'] = provincia
                else:
                    entrada_db['provincia'] += ", "+provincia
            if comunidad is not None:
                if indice == 0:
                    entrada_db['comunidad'] = comunidad
                else:
                    entrada_db['comunidad'] += ", "+comunidad
            if pais is not None:
                if indice == 0:
                    entrada_db['pais'] = pais
                else:
                    entrada_db['pais'] += ", "+pais
            indice += 1
        mongodb.add_update_element(database,entrada_db)
    return


#TODO ver que hacer con esto, si meterlo en nuestra propia db o no, ya que podemos usar al externa
def infojobs_DB():
    #skills_db = mongodb.get_db(database_ip, database_port, database_habilidades)
    req = requests.get('https://api.infojobs.net/api/1/dictionary/type/skills',
                       auth=('2fe25988a01f48c59b36425abd6329b8', 'DHn5nyC8m1ByxAT1tnJUHjmwr4oZuYV82vVKlXqOKdCh6h4E05'))
    if req.status_code is 200:
        res_json = req.json()
        #print res_json
        for skill in res_json:
            if 'java' in skill['name'].lower():
                print(skill['name'].lower())
            #mongodb.add_update_element(skills_db, skill)

    '''req = requests.get('https://api.infojobs.net/api/1/dictionary/type/certifications',
                        auth=('2fe25988a01f48c59b36425abd6329b8', 'DHn5nyC8m1ByxAT1tnJUHjmwr4oZuYV82vVKlXqOKdCh6h4E05'))
    if req.status_code is 200:
        res_json = req.json()
        for skill in res_json:
            print(skill)

    req = requests.get('https://api.infojobs.net/api/1/dictionary/type/InformalTraining',
                        auth=('2fe25988a01f48c59b36425abd6329b8', 'DHn5nyC8m1ByxAT1tnJUHjmwr4oZuYV82vVKlXqOKdCh6h4E05'))
    if req.status_code is 200:
        res_json = req.json()
        for skill in res_json:
            print(skill)

    #req = requests.get('https://api.infojobs.net/api/1/dictionary/study-detail',
    #                   auth=('2fe25988a01f48c59b36425abd6329b8', 'DHn5nyC8m1ByxAT1tnJUHjmwr4oZuYV82vVKlXqOKdCh6h4E05'))
    #if req.status_code is 200:
    #    res_json = req.json()
    #    print(res_json)'''





#TODO Consultas SPARQL???????
'''def search_sparql(word):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(
        """    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               SELECT * WHERE { <http://dbpedia.org/resource/""" + word + """>
               rdf:type dbo:Software FILTER(langMatches(lang(?abstract), "es"))}""")
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def print_result(results):
    for result in results["results"]["bindings"]:
        print(result["abstract"]["value"])
    return'''

def main():
    #infojobs_DB()
    actualizar_localizacion(mongodb.get_db(database_ip, database_port, database_ofertas))
    #actualizar_localizacion(mongodb.get_db(database_ip, database_port, database_usuarios))
    '''results = search_sparql("Asturias")
    print_result(results)
    results = search_sparql("Microsoft_Windows")
    print_result(results)
    results = search_sparql("Java")
    print_result(results)
    results = search_sparql("C++")
    print_result(results)
    results = search_sparql("Spain")
    print_result(results)'''
    return


if __name__ == "__main__":
    main()