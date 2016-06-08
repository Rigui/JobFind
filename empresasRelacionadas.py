import mongodb


def relacionadas(colOfer, colTit):
    ofertas = colOfer.find()

    for oferta in ofertas:
        relac = set()
        nivTit = oferta["nivel_titulacion"]

        # parecidas = []
        # for i in range(0, nivTit):
        #     ret = colOfer.find({"nivel_titulacion": i})
        #     for r in ret:
        #         parecidas.append(r)

        parecidas = colOfer.find()

        for p in parecidas:
            parImp, parCom = ratioParecidoReq(oferta, p)
            parTit = ratioParecidoTitulacion(oferta, p, colTit)
            val = (0.8 * parImp + 0.2 * parCom)  # / 2 + parTit / 2
            if val >= 0.2:
                if p['empresa'] != oferta['empresa']:
                    relac.add(p['empresa'])

        oferta["empresasRelacionadas"] = list(relac)

        colOfer.save(oferta)


def ratioParecidoReq(oferta, comparacion):
    impComp = comparacion["imprescindible"]
    competComp = comparacion["competencias"]

    impOf = oferta["imprescindible"]
    comOf = oferta["competencias"]

    nImp = nCom = 0

    if len(impOf) > 0:
        for imp in impOf:
            if imp in impComp:
                nImp += 1

    if len(comOf) > 0:
        for com in comOf:
            if com in competComp:
                nCom += 1
    if not impOf and not comOf:
        return 0, 0
    elif not impOf and len(comOf) > 0:
        return 0, (nCom / len(comOf))
    elif len(impOf) > 0 and not comOf:
        return (nImp / len(impOf)), 0
    else:
        return (nImp / len(impOf)), (nCom / len(comOf))


def ratioParecidoTitulacion(oferta, comparativa, colTit):
    titulos = colTit.find()[0]["value"]
    for tit in titulos:
        tit = tit[0:len(tit) - 4]
    coinc = []

    titOf = oferta["titulacion"]
    reqOf = oferta["requisitos"]
    catOf = oferta["categoria"]
    subcatOf = oferta["subcategoria"]
    nameOf = oferta["titulo_oferta"]

    titCom = comparativa["titulacion"]
    reqCom = comparativa["requisitos"]
    catCom = comparativa["categoria"]
    subcatCom = comparativa["subcategoria"]
    nameCom = comparativa["titulo_oferta"]

    titulosOf = titulosOferta(titulos, reqOf, catOf, subcatOf, nameOf, titOf)
    titulosCom = titulosOferta(titulos, reqCom, catCom, subcatCom, nameCom, titCom)

    for t in titulosOf:
        if t in titulosCom:
            coinc.append(t)
    if len(titulosOf) == 0:
        return 0
    else:
        return len(coinc) / len(titulosOf)


def titulosOferta(titulos, req, cat, subcat, name, tit):
    titOf = set()
    for t in titulos:
        if " " in t:
            palabras = t.split(" ")
            nPal = len(palabras) - 1
            if cat is not None:
                for i, j in enumerate(cat):
                    if j == palabras[0]:
                        cont = 0
                        for s in range(1, nPal):
                            if cat[i + s] != palabras[nPal]:
                                cont = 1
                        if cont == 0:
                            titOf.add(t)
            if subcat is not None:
                for i, j in enumerate(subcat):
                    if j == palabras[0]:
                        cont = 0
                        for s in range(1, nPal):
                            if cat[i + s] != palabras[nPal]:
                                cont = 1
                        if cont == 0:
                            titOf.add(t)
            if name is not None:
                for i, j in enumerate(name):
                    if j == palabras[0]:
                        cont = 0
                        for s in range(1, nPal):
                            if cat[i + s] != palabras[nPal]:
                                cont = 1
                        if cont == 0:
                            titOf.add(t)
            if tit is not None:
                for i, j in enumerate(tit):
                    if j == palabras[0]:
                        cont = 0
                        for s in range(1, nPal):
                            if cat[i + s] != palabras[nPal]:
                                cont = 1
                        if cont == 0:
                            titOf.add(t)

        else:
            if cat is not None and not cat:
                for c in cat:
                    if t in c:
                        titOf.add(t)
            if subcat is not None and not subcat:
                for s in subcat:
                    if t in s:
                        titOf.add(t)
            if name is not None and not name:
                for n in name:
                    if t in n:
                        titOf.add()
            if tit is not None and not tit:
                for ti in tit:
                    if t in ti:
                        titOf.add(t)

        if req is not "" and t in req:
            titOf.add(t)
    return list(titOf)
