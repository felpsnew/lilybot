from ast import Return
from itertools import count
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from time import time, sleep
import sys
import numpy as np
from logg import *
from talib.abstract import BBANDS, EMA
import pandas as pd
from candlestick import candlestick
from Indicador_tecnico import humor
from tetx import mhivdd
status = ()
id = ()

def bolinger(taxa_ou_ema):  #REALIZA A COMPRA OU VENDA DAS MEDIAS BOLLINGER OU EMA 
	res = ''
	if taxa_ou_ema >= up or taxa_ou_ema <= low:
		if taxa_ou_ema >= up:
			res = 'put'
		else:
			res = 'call'

		print(res,'MB')

	return res
	

def pattern_call(res_call): #REALIZA A COMPRA DOS CONDLES DE TENDENCIA DE ALTA
	res = ''
	trabalhando = res_call.to_dict('records')
	for data in trabalhando:
		if data['result'] == True:
			res = 'call'
			print(res,'CC')
	
	return res
	

def pattern_put(res_put): #REALIZA A COMPRA DOS CANDLES DE TENDENCIA DE QUEDA
	res = ''
	trabalhando = res_put.to_dict('records')
	for data in trabalhando:
		if data['result'] == True:
			res = 'put'
			print(res,'CP')
	return res


def soma(a,b,c,d,e,f):
	res = ['']
	len(res)
	res = a + b + c + d + e + f	
	return res


cabeçalho('Versão 0.2')

API, par, timeframe, usuario = logg()	#DEF QUE IMPORTA DADOS DO USUARIO	
tipo_mhi = int(input(' Voce deseja que eu opere a favor da Maioria ou Minoria?\n  Digite 1 para minoria\n  Digite 2 para maioria\n  :: '))

velas_q = 101
operacao = 200

while True:
	
	inicio = time()
	
	velas_p = API.get_candles(par, 60, 2, int(time()))#GET CANDLES FOR CANDLES PATTERN
	candles_df = pd.DataFrame.from_dict(velas_p)
	candles_df.rename(columns={"max": "high", "min": "low"}, inplace=True)

	#-------------------------------------------------------------------------------------
	res_dark_cloud_cover = candlestick.dark_cloud_cover(candles_df, target='result')
	res_bullish_engulfing = candlestick.bullish_engulfing(candles_df, target='result')
	#---------------------------------------------------------------------------------------
	velas = API.get_candles(par, 60, velas_q, time())

	dados_f = {
				'open': np.empty(velas_q),
				'high': np.empty(velas_q), 
				'low': np.empty(velas_q),
				'close': np.empty(velas_q),
				'volume': np.empty(velas_q)
	}
	
	for x in range(0, velas_q):
		dados_f['open'][x] = velas[x]['open']
		dados_f['high'][x] = velas[x]['max']
		dados_f['low'][x] = velas[x]['min']
		dados_f['close'][x] = velas[x]['close']
		dados_f['volume'][x] = velas[x]['volume']
	
	up, mid, low = BBANDS(dados_f, timeperiod=30, nbdevup=2.0, nbdevdn=2.0, matype=0)
	
	velaant = dados_f['close'][20]

	up = round(up[ len(up)-2 ], 6)
	low = round(low[ len(low)-2 ], 6)
	taxa_atual = round(velas[-1]['close'], 6)
#------------------------------------------------------

	#Calculo EMA TA-Lib
	calculo_ema = EMA(dados_f, timeperiod=100)
	calculo_ema = round(calculo_ema[-1],6)

#------------------------------------------------------------------------ CALCULO MALUCO DO FELIPEE

	if (velaant - taxa_atual) > 0.003 or (taxa_atual - velaant) > 0.003:
		tendencia = 'put' if velaant > taxa_atual else 'call' 
	else: 
		tendencia = 'Lateralizado'
		
#-------------------------------------------------- REALIZA O CALCULO DA QUANDO A TAXA ATUAL SAI DA BANDA DE BOLLINGER

	#out_low = 0
	#out_up = 0
	#if taxa_atual > low:
	#	out_low = abs(round((low * 100) - (taxa_atual * 100),3))
	#if taxa_atual < up:
	#	out_up = abs(round((taxa_atual * 100) - (up * 100),3))

	print('Taxa:', taxa_atual, 
			'| Time:', round(time() - inicio, 2), 'seg',
			'| TVela:', datetime.fromtimestamp( int(velas[-1]['from']) ).strftime('%H:%M'),
	)

#========================================================================================================================

#ENTRADA

#======================================================================================================================
	#if dir:
	res_bolinger = bolinger(taxa_atual)
	res_ema = bolinger(calculo_ema)
	res_candy_put = pattern_put(res_dark_cloud_cover)
	res_candy_call = pattern_call(res_bullish_engulfing)
	res_humor = humor(API, par)
	res_mhi = mhivdd(API, par, tipo_mhi)
	res = soma(res_bolinger, res_ema, res_candy_call, res_candy_put, res_humor, res_mhi)
	print('CALLs: ',res.count('call'),'PUTs: ',res.count('put'))

	if res.count('call') >= 2:
		print('Realizando entrada na taxa', taxa_atual)
		status, id = API.buy_digital_spot(par, 2000,'call', 1)
		if status:
			print('Entrada realizada com sucesso, aguardando resultado..')
			
			while True:
				status, valor = API.check_win_digital_v2(id)
				
				if status:
					
					if valor < 0 : valor = -2
					
					print('Resultado da operação: ', end='')
					
					if valor > 0:
						print('WIN! +' + str(valor))
					else:
						print('LOSS!', valor)

					break
		sleep(0.5)


	if res.count('put') >=2:
		print('Realizando entrada na taxa', taxa_atual)
		status, id = API.buy_digital_spot(par, 2000,'put', 1)
		if status:
			print('Entrada realizada com sucesso, aguardando resultado..')
			
			while True:
				status, valor = API.check_win_digital_v2(id)
				
				if status:
					
					if valor < 0 : valor = -2
					
					print('Resultado da operação: ', end='')
					
					if valor > 0:
						print('WIN! +' + str(valor))
					else:
						print('LOSS!', valor)

					break

		sleep(0.5)

