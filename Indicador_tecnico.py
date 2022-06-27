from click import version_option


def humor (API,par):
    from opcode import haslocal
    from iqoptionapi.stable_api import IQ_Option
    from datetime import datetime
    from time import time, sleep
    import sys
    import numpy as np
    from talib.abstract import EMA
    import copy
    from decimal import Decimal

    tendencia = ''
    microtendencia = ''
    velas = API.get_realtime_candles(par, 60)

    dados_t =   {'open': np.array([]), 
                'high': np.array([]), 
                'low': np.array([]), 
                'close': np.array([]), 
                'volume': np.array([]) }

    velas_copia = copy.copy(velas)

    for x in velas_copia:
            dados_t['open'] = np.append(dados_t['open'], velas_copia[x]['open'])
            dados_t['high'] = np.append(dados_t['high'], velas_copia[x]['max'])
            dados_t['low'] = np.append(dados_t['low'], velas_copia[x]['min'])
            dados_t['close'] = np.append(dados_t['close'], velas_copia[x]['close'])
            dados_t['volume'] = np.append(dados_t['volume'], abs(Decimal(str(velas_copia[x]['open']))-Decimal(str(velas_copia[x]['close']))))
        
    tendencia1 = EMA(dados_t, timeperiod=100)
    tendencia2 = round(tendencia1[-2],5)
    ema = round(tendencia1[-1],5)
    tendencia3 = round(tendencia1[-10],5) 
    microtendencia1 = EMA(dados_t, timeperiod=10)
    microtendencia2 = round(microtendencia1[-2],5)
    microtendencia3 = round(microtendencia1[-4],5) 
    volume = round(dados_t['volume'][-2],5)

    if tendencia3 > tendencia2 or tendencia2 > tendencia3:
        if tendencia3 > tendencia2:
            tendencia = 'put'
        if tendencia3 < tendencia2:
            tendencia = 'call'
    else:
        tendencia = 'Lateralizado'

    if microtendencia3 > microtendencia2 or microtendencia2 > microtendencia3:
        if microtendencia3 > microtendencia2:
            microtendencia = 'put'
        if microtendencia3 < microtendencia2:
            microtendencia = 'call'
    else:
        microtendencia = 'Lateralizado'


    #print('Tendencia: ',diferenca1)
    #print(vol1,vol2,volume)
    
    return tendencia, microtendencia,volume,ema

def suporte_resistencia (API,par):
    import pandas as pd
    import numpy as np
    
    df = API.get_realtime_candles(par, 60)
    
    def isSupport(velas,i):
        support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
        return support

    def isResistance(df,i):
        resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
        return resistance

    levels = []
    for i in range(2,df.volume[0]-2):
        if isSupport(df,i):
            levels.append((i,df['Low'][i]))
        elif isResistance(df,i):
            levels.append((i,df['High'][i]))
    
    return levels