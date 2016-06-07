from pymongo import MongoClient


def get_db(database_ip, database_port, database_name):
    client = MongoClient(database_ip, database_port)
    ofertasdb = client.get_database(database_name)
    db = ofertasdb[database_name]
    return db


def add_update_element(db, oferta):
    db.save(oferta)


def get_element(db, query=None):
    if query is None:
        query = {}
    return db.find(query)


def remove_oferta(db, id_element):
    db.remove(id_element)
