from ast import Return
from itertools import count
#from signal import pause
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from time import time
import linecache 
import sys
import numpy as np
from logg import *
import pandas as pd
from candlestick import candlestick
from Indicador_tecnico import humor
from str_mhi import mhivdd
from mhihiper import mhiGale
from bollinger import bolling 
import json
import os
from tqdm import tqdm

secdir = False
dir = False
lucro = 0
win = 0
loss = 0
mhiGaleB = False
galee = 0
lo = ['.']

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


print('''

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

cabeçalho('Versão 0.7')

user = linecache.getline('config.txt',15)
password = linecache.getline('config.txt',16)

API, timeframe, usuario = logg(user,password)	#DEF QUE IMPORTA DADOS DO USUARIO

def perfil():
	perfil = json.loads(json.dumps(API.get_profile_ansyc()))
	return perfil

x = perfil()

print('ID:', x['user_id'])
print(x['name'])
banca(API)
pares = API.get_all_open_time()
print(' PARIDADES DIGITAL: \n')
for paridade in pares['digital']:
	if pares['digital'][paridade]['open'] == True:
		payout = API.get_digital_payout(paridade)
		print(' ',paridade+' | PAYOUT: ',payout,'%')

par = paridad()

entrada = linecache.getline('config.txt',7)
stop_l = linecache.getline('config.txt',8)
stop_w = linecache.getline('config.txt',9)
gale_c = linecache.getline('config.txt',10)

valor_entrada_b, stop_loss, stop_win, martingale = valores(entrada,stop_l,stop_w,gale_c)

#tipo_mhi = int(input(' Voce deseja que eu opere a favor da Maioria ou Minoria?\n  Digite 1 para minoria\n  Digite 2 para maioria\n  :: '))

payout = Pay(API, par)

print('\n LOADING...' )

API.start_candles_stream(par, 60, 900)

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
	res_candy_put = pattern_put(res_dark_cloud_cover)
	res_candy_call = pattern_call(res_bullish_engulfing)
	res_humor, microtendencia, volume, ema = humor(API, par)
	res_bollinger,taxa_atual = bolling(API, par,ema)
	res_mhi = mhiGale(API, par)
	res = soma(res_candy_put,res_candy_call,res_mhi)

	os.system('cls') #LIMPAR TELA DE COMANDO
	
	if lo.count('.') == 3:
		lo = ['.']
	else:
		lo.append('.')

	print('ANALISANDO VELAS\nAguarde',*lo,
		'\nCALLs: ',res.count('call'),
		' | PUTs: ',res.count('put'),
		'\nLucro: ',round(lucro, 2),
		' | Par: ',par,
		'\nValor de entrada: ',valor_entrada_b,
		'\nIndicador: ', res_humor,
		'\nVolume Ultima Vela fechada: ', volume,
		'\nTaxa Atual: ', taxa_atual,
		'\nLily Delay:', round(time() - inicio, 2), 'seg')

	if res.count('call') >= 1 or res.count('put') >= 1:
		dir = 'call' if res.count('call') >= 1	 else 'put'
	else:
		dir = False

	if dir:
		print('Direção: ',dir)
			
		valor_entrada = valor_entrada_b
		for i in range(martingale):
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
						print('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2) ,'/ Lucro', round(lucro, 2),('/ '+str(i)+ ' GALE' if i > 0 else '' ))
						# 1 GAlE = MHi | 2 Gale = inversão | 3 GALE = inversão
						
						galee = +1 if valor < 0 else 0
						if galee <4:
							mhiGaleB = False
							dir = 'put' if dir == 'call' else 'call'
						valor_entrada = Martingale(valor_entrada, payout)

						stop(lucro, stop_win, stop_loss)

						break
						
				if valor > 0 : break
				
			else:
				print('\nERRO AO REALIZAR OPERAÇÃO\n\n')