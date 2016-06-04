import scrapping_uvigo
import infojobs
import mongodb

print "Prueba.py\n"

print "Obtener base de datos"
ofertas_db = mongodb.get_db()

print "\nObtener ofertas de Uvigo"
ofertas_uvigo = scrapping_uvigo.get_uvigo()
for oferta_uvigo in ofertas_uvigo:
    mongodb.add_oferta(ofertas_db, oferta_uvigo)
    print oferta_uvigo

print "\nObtener ofertas de Infojobs"
ofertas_infojobs = infojobs.get_infojobs()
for each_oferta in ofertas_infojobs:
    mongodb.add_oferta(ofertas_db, each_oferta)
    print each_oferta
