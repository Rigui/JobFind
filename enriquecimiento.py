import mongodb
import empresasRelacionadas as Emp
import generarExperiencia as Gen


def enriquecimiento():
    database_ip = "52.208.8.144"
    database_port = 8080

    colOfer = mongodb.conectar(database_ip, database_port, "ofertas")
    colReq = mongodb.conectar(database_ip, database_port, "requisitos")
    colTit = mongodb.conectar(database_ip, database_port, "titulos")
    docs = colOfer.find({'experiencia_min': {'$type': 10}})

    print("inicio exp")
    for doc in docs:
        Gen.generarExperiencia(colOfer, doc)
    print("inicio relaciones")
    Emp.relacionadas(colOfer, colReq, colTit)
