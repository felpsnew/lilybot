from ast import Return
from itertools import count
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from time import time ,sleep
import sys
import numpy as np
from logg import *
import pandas as pd
from candlestick import candlestick
from Indicador_tecnico import humor
from str_mhi import mhivdd, mhiGale
from bollinger import bolling 
import json
import os
dir = False
lucro = 0
win = 0
loss = 0
mhiGaleB = False

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

def soma(a = '',b = '',c = '',d = '',e = '',f = ''):
	res = ['']
	len(res)
	res = a + b + c + d + e + f	
	return res


print('\033[91m','''

                       ,--,                
                    ,---.'|                
  ,--,              |   | :                
,--.'|      ,--,    :   : |                
|  | :    ,--.'|    |   ' :                
:  : '    |  |,     ;   ; '                
|  ' |    `--'_     '   | |__        .--,  
'  | |    ,' ,'|    |   | :.'|     /_ ./|  
|  | :    '  | |    '   :    ;  , ' , ' :  
'  : |__  |  | :    |   |  ./  /___/ \: |  
|  | '.'| '  : |__  ;   : ;     .  \  ' |  
;  :    ; |  | '.'| |   ,/       \  ;   :  
|  ,   /  ;  :    ; '---'         \  \  ;  
 ---`-'   |  ,   /                 :  \  \ 
           ---`-'                   \  ' ; 
                                     `--`  
                                    `--`                                             
''')

cabeçalho('Versão 0.6')

API, timeframe, usuario = logg()	#DEF QUE IMPORTA DADOS DO USUARIO

def perfil():
	perfil = json.loads(json.dumps(API.get_profile_ansyc()))
	return perfil

x = perfil()

print('\033[93m','ID:', x['user_id'])
print('\033[93m',x['name'])
banca(API)
pares = API.get_all_open_time()
print('\033[93m',' PARIDADES DIGITAL: \n')
for paridade in pares['digital']:
	if pares['digital'][paridade]['open'] == True:
		payout = API.get_digital_payout(paridade)
		print('\033[93m',' ',paridade+' | PAYOUT: ',payout,'%')

par = paridad()

valor_entrada_b, stop_loss, stop_win, martingale = valores()

tipo_mhi = int(input(' Voce deseja que eu opere a favor da Maioria ou Minoria?\n  Digite 1 para minoria\n  Digite 2 para maioria\n  :: '))

payout = Pay(API, par)

print('\033[0m','\n LOADING...' )

API.start_candles_stream(par, 60, 720)

while True:
	
	inicio = time()
	
	velas_p = API.get_candles(par, 60, 2, int(time()))#GET CANDLES FOR CANDLES PATTERN
	candles_df = pd.DataFrame.from_dict(velas_p)
	candles_df.rename(columns={"max": "high", "min": "low"}, inplace=True)


	res_dark_cloud_cover = candlestick.dark_cloud_cover(candles_df, target='result')
	res_bullish_engulfing = candlestick.bullish_engulfing(candles_df, target='result')

#========================================================================================================================

#ENTRADA

#======================================================================================================================
	res_bollinger = bolling(API, par)
	res_candy_put = pattern_put(res_dark_cloud_cover)
	res_candy_call = pattern_call(res_bullish_engulfing)
	res_humor, microtendencia = humor(API, par)
	res_mhi = mhivdd(API, par, tipo_mhi)
	res = soma(res_humor, res_bollinger, res_candy_call, res_candy_put, res_mhi)

	os.system('clear') or None #LIMPAR TELA DE COMANDO

	print('\033[42m'+'\033[1m'+'\033[30m'+
		'ANALISANDO VELAS\nAguarde:',
		'\nCALLs: ',res.count('call'),
		' | PUTs: ',res.count('put'),
		'\nLucro: ',round(lucro, 2),
		' | Par: ',par,
		' | Indicador: ', res_humor,
		'\nLily Delay:', round(time() - inicio, 2), 'seg'
		+'\033[0;0m')

	if res.count('call') >= 2 or res.count('put') >= 2:
		dir = 'call' if res.count('call') >=2 else 'put'
	else:
		dir = False

	if dir:
		print('Direção: ',dir)
			
		valor_entrada = valor_entrada_b
		for i in range(martingale+1):
			mhigale = mhiGale(API, par)

			if mhiGaleB == True:
				dir = mhigale
				status,id = API.buy_digital_spot_v2(par, valor_entrada, dir, 1)
				mhiGaleB = False
			else:	
				status,id = API.buy_digital_spot_v2(par, valor_entrada, dir, 1)
			
			if status:
				while True:
					status,valor = API.check_win_digital_v2(id)
					
					if status:
						valor = valor if valor > 0 else float('-' + str(abs(valor_entrada)))
						lucro += round(valor, 2)
						
						print('Resultado operação: ', end='')
						print('\033[92m','WIN /' if valor > 0 else '\033[91m','LOSS /' , round(valor, 2) ,'/ Lucro', round(lucro, 2),('/ '+str(i)+ ' GALE' if i > 0 else '' ), "MHIO: ", mhigale)
						
						mhiGaleB = True if valor < 0 else False
						valor_entrada = Martingale(valor_entrada, payout)
						stop(lucro, stop_win, stop_loss)

						break

					#dir = False
						
				if valor > 0 : break
				
			else:
				print('\nERRO AO REALIZAR OPERAÇÃO\n\n')


	sleep(0.3)
