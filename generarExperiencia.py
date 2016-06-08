def generarExperiencia(col, doc):
    imprescindible = doc['imprescindible']
    competencias = doc['competencias']

    nivTit = doc['nivel_titulacion']
    if nivTit == 0:
        nivXP = (0.8 * (0.75 * valoracionRequisitos(len(imprescindible))) +
                 0.25 * valoracionRequisitos(len(competencias)))
    else:
        nivXP = (0.2 * 1 / nivTit + 0.8 * (0.75 * valoracionRequisitos(len(imprescindible))) +
                 0.25 * valoracionRequisitos(len(competencias)))
    xp = int(nivXP * 10)
    doc["experiencia_min"] = xp
    col.save(doc)


def valoracionRequisitos(long):
    if long < 2:
        return 0.1
    elif 2 <= long < 4:
        return 0.2
    elif 4 <= long < 6:
        return 0.3
    elif 6 <= long < 8:
        return 0.4
    elif 6 <= long < 10:
        return 0.5
    elif 10 <= long < 12:
        return 0.6
    elif 12 <= long < 14:
        return 0.7
    elif 14 <= long < 16:
        return 0.8
    elif 16 <= long < 18:
        return 0.9
    else:
        return 1
