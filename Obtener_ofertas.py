import scrapping_uvigo
import infojobs
import mongodb

database_ip = "52.208.8.144"
database_port = 27017
database_ofertas = "ofertas"

def obtener_ofertas():
    print "Obtener base de datos"
    ofertas_db = mongodb.get_db(database_ip, database_port, database_ofertas)

    print "Obtener ofertas de Uvigo"
    ofertas_uvigo = scrapping_uvigo.get_uvigo()
    for oferta_uvigo in ofertas_uvigo:
        mongodb.add_update_element(ofertas_db, oferta_uvigo)

    print "Obtener ofertas de Infojobs"
    ofertas_infojobs = infojobs.get_infojobs()
    for each_oferta in ofertas_infojobs:
        mongodb.add_update_element(ofertas_db, each_oferta)

    return
