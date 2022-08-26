def bolling (API, par, ema):
    from iqoptionapi.stable_api import IQ_Option
    from datetime import datetime
    from time import time 
    import sys
    import numpy as np
    from talib.abstract import BBANDS
    import copy

    dir = ''
    go = False
    velas = API.get_realtime_candles(par, 60)

    dados_f = {'open': np.array([]), 
                'high': np.array([]), 
                'low': np.array([]), 
                'close': np.array([]), 
                'volume': np.array([]) }

    velas_copia = copy.copy(velas)

    for x in velas_copia:
            dados_f['open'] = np.append(dados_f['open'], velas_copia[x]['open'])
            dados_f['high'] = np.append(dados_f['high'], velas_copia[x]['max'])
            dados_f['low'] = np.append(dados_f['low'], velas_copia[x]['min'])
            dados_f['close'] = np.append(dados_f['close'], velas_copia[x]['close'])
            dados_f['volume'] = np.append(dados_f['volume'], velas_copia[x]['volume'])
       


    up, mid, low = BBANDS(dados_f, timeperiod=16, nbdevup=2.0, nbdevdn=2.0, matype=0)
    #up_b, mid_b, low_b = BBANDS(dados_f, timeperiod=16, nbdevup=2.1, nbdevdn=2.1, matype=0)

    up = round(up[ len(up)-1 ], 5)
    low = round(low[ len(low)-1 ], 5)
    taxa_atual = round(dados_f['close'][-1], 6)

    #up_b = round(up_b[ len(up_b)-2 ], 5)
    #low_b = round(low_b[ len(low_b)-2 ], 5)

    ema2 = round(ema * 0.0002,5)
    emaup = round(ema + ema2,5)
    emalow = round(ema - ema2,5)
    #print('EMA:', ema,'\nEMA UP',emaup,'\nEMA LOW',emalow,'\nUP: ',up,'\nLow: ',low)

    #if taxa_atual > up_b or taxa_atual < low_b:
    #    go = False
    #else:
    #    go = True

    #if go:

    if taxa_atual >= up and emalow < low:
        dir = 'put'
        print('BB Put')


    if taxa_atual <= low and emaup > up:
        dir = 'call'
        print('BB Call')
    
    return dir,taxa_atual