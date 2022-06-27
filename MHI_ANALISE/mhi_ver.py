from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from time import time, sleep
import sys
from logg import logg

API, timeframe, usuario = logg()
# Backtest MHI M1
# Minoria
# Até 2 Martingales

while True:
	win = 0
	loss = 0
	doji = 0
	mg1 = 0
	mg2 = 0
	
	print('\n\n Qual paridade analisar? ', end='')
	par = str(input().strip()).upper()
	
	candles = API.get_candles(par, 60, 1000, int(time()))
	
	for index, vela in enumerate(candles):
		
		min = int(datetime.fromtimestamp(int(vela['from'])).strftime('%M')[1:])
		
		if min == 5 or min == 0:
			
			cor_operacao = 'g' if vela['open'] < vela['close'] else 'r' if vela['open'] > vela['close'] else 'd'
			
			entrada_analise = ['g' if candles[index - i]['open'] < candles[index - i]['close'] else 'r' if candles[index - i]['open'] > candles[index - i]['close'] else 'd' for i in range(1, 4)]
			entrada_analise = False if entrada_analise.count('d') > 0 else 'g' if entrada_analise.count('r') > entrada_analise.count('g') else 'r' if entrada_analise.count('g') > entrada_analise.count('r') else False
			
			if entrada_analise != False:
			
				if entrada_analise == cor_operacao:
					win += 1
					
				else:
					
					try:
						mg1_res = 'g' if candles[index + 1]['open'] < candles[index + 1]['close'] else 'r' if candles[index + 1]['open'] > candles[index + 1]['close'] else 'd'
					except:
						mg1_res = False
					
					try:
						mg2_res = 'g' if candles[index + 2]['open'] < candles[index + 2]['close'] else 'r' if candles[index + 2]['open'] > candles[index + 2]['close'] else 'd'
					except:
						mg2_res = False
					
					if mg1_res == cor_operacao and mg1_res != False:
						mg1 += 1					
					elif mg2_res == cor_operacao and mg1_res != False:
						mg2 += 1					
					else:						
						loss += 1
						
						if mg1_res != False : loss += 1
						if mg2_res != False : loss += 1
						
			else:
				doji += 1						
	
	print('\n\n ----------[ Resultado ]----------')
	print(' WIN MÃO FIXA:', win)
	print(' WIN MARTINGALE 1:', mg1)
	print(' WIN MARTINGALE 2:', mg2)
	print(' LOSS:', loss)
	print(' ENTRADAS NÃO REALIZADAS:', doji)
	print(' WINRATE:', round(100 * ((win + mg1 + mg2) / (win + mg1 + mg2 + loss))), '%')
	print(' TOTAL DE OPERAÇÕES:', win + mg1 + mg2 + loss, '\n\n')
	