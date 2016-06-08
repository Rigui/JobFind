import opBasicas
import empresasRelacionadas as Emp
import generarExperiencia as Gen


# import generarExperiencia as Gen


def enriquecimiento():
    col = opBasicas.conectar()
    docs = col.find({'expMinima': {'$type': 10}})
    # docs = col.find()
    print("inicio exp")
    for doc in docs:
        Gen.generarExperiencia(col, doc)
    print("inicio relaciones")
    Emp.relacionadas(col)


enriquecimiento()
