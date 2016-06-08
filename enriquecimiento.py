import mongodb
import empresasRelacionadas as Emp
import generarExperiencia as Gen


def enriquecimiento():
    database_ip = "52.208.8.144"
    database_port = 8080

    colOfer = mongodb.get_db(database_ip, database_port, "ofertas")
    colTit = mongodb.get_db(database_ip, database_port, "titulos")
    # rellena la experiencia de aquellas que no lo tengan (no actualiza -> el objetivo es completar, no inventar)
    docs = colOfer.find({'experiencia_min': {'$type': 10}})

    cont = 0
    print("inicio exp")
    for doc in docs:
        Gen.generarExperiencia(colOfer, doc)
        cont += 1
        print cont
    print("inicio relaciones")
    Emp.relacionadas(colOfer, colTit)

enriquecimiento()