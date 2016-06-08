def relacionadas(col):
    ofertas = col.find()
    cont = 0
    for oferta in ofertas:
        req = oferta["requisitos"]
        cReq = len(req)
        parecidas = col.find({"categoria": oferta["categoria"], "titulacion": oferta["titulacion"],
                              "nivel_titulacion": oferta["nivel_titulacion"]})

        relac = []

        for p in parecidas:
            reqp = p["requisitos"]
            coincidencias = 0
            for r in reqp:
                if r in req:
                    coincidencias += 1
            if (coincidencias / cReq) >= 0.8 and p["empresa"] not in relac:
                relac.append(p["empresa"])

        oferta["empresasRelacionadas"] = relac

        col.save(oferta)

        cont += 1
