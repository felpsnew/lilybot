def mhiGale (API, par):
    from glob import glob
    from iqoptionapi.stable_api import IQ_Option
    from datetime import datetime


    dir = ''
    inverte = False
    minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
    entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
    
    
    if entrar:
        print("Verificando cores..")  # Aplica Estratégia MHI Potencializada
        velas = API.get_candles(par, 60, 10, API.get_server_timestamp())

        velas[2] = (
            "g"
            if velas[2]["open"] < velas[2]["close"] and velas
            else "r"
        )
        velas[3] = (
            "g"
            if velas[3]["open"] < velas[3]["close"]
            else "r"
        )
        velas[4] = (
            "g"
            if velas[4]["open"] < velas[4]["close"]
            else "r"
        )
        velas[5] = (
            "g"
            if velas[5]["open"] < velas[5]["close"]
            else "r"
        )
        velas[6] = (
            "g"
            if velas[6]["open"] < velas[6]["close"]
            else "r"
        )
        velas[7] = (
            "g"
            if velas[7]["open"] < velas[7]["close"]
            else "r"
        )
        velas[8] = (
            "g"
            if velas[8]["open"] < velas[8]["close"]
            else "r"
        )
        velas[9] = (
            "g"
            if velas[9]["open"] < velas[9]["close"]
            else "r"
        )

        cores1 = velas[2] + " " + velas[3] + " " + velas[4]

        if cores1.count("g") > cores1.count("r"):
            next = "r"
            if velas[5] != next and velas[6] != next:
                inverte = True
            else:
                inverte = False

        if cores1.count("r") > cores1.count("g"):
            next = "g"
            if velas[5] != next and velas[6] != next:
                inverte = True
            else:
                inverte = False

        cores2 = velas[7] + " " + velas[8] + " " + velas[9]

        if 3 > cores2.count("g") > cores2.count("r"):
            if not inverte:
                dir = "put"
            else:
                dir = "call"
        else: 
            dir = "call"

        if 3 > cores2.count("r") > cores2.count("g"):
            if not inverte:
                dir = "call"
            else:
                dir = "put"
        else:
            dir = "put"

        print(
            "Primeiro Quadrante:",
            cores1,
            "\nCandle:",
            velas[5],
            velas[6],
            "\nSegundo Quadrante:",
            cores2,
            "\nInverteu?",
            inverte,
            "\nSentido:",
            dir,
        )

    return dir