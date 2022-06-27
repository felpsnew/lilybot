
def logg (user,password):
	from iqoptionapi.stable_api import IQ_Option
	import sys
	mainUser = {
	'username': "na",
	'password': "na"
	}
	mainUser['username'] = str.strip(user)
	mainUser['password'] = str.strip(password)
	usuario = mainUser

	API = IQ_Option(usuario["username"], usuario["password"])   

	API.connect()

	API.change_balance('PRACTICE') # PRACTICE / REAL

	if API.check_connect():
		print('\033[92m','\n\nConectado com sucesso')
	else:
		print('\033[92m','\n Erro ao se conectar')
		sys.exit()

	timeframe = 60

	return API, timeframe, usuario

def perfil(API):
	import json
	perfil = json.loads(json.dumps(API.get_profile_ansyc()))
	return perfil['result']

def stop(lucro, gain, loss):
	import sys
	
	#stoplucro = round((lucro - gain),2) 
	#print(stoplucro)

	if lucro <= float('-' + str(abs(loss))):
		print('Stop Loss batido!')
		sys.exit()
		
	if lucro >= float(abs(gain)):
		print('Stop Gain Batido!')
		sys.exit()

	
def Martingale(valor, payout):
	lucro_esperado = valor * payout
	perca = float(valor)	
		
	while True:
		if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
			return round(valor, 2)
			break
		valor += 0.01

def Payout(API,par, tipo ='digital', timeframe = 1):
	from time import sleep
	if tipo == 'turbo':
		a = API.get_all_profit()
		return int(100 * a[par]['turbo'])
		
	elif tipo == 'digital':
	
		API.subscribe_strike_list(par, timeframe)
		while True:
			d = API.get_digital_current_profit(par, timeframe)
			if d != False:
				d = round(int(d) / 100,2)
				break
			sleep(1)
		API.unsubscribe_strike_list(par, timeframe)
		return d

def linha(tam = 80):
    return '-' * tam

def cabeçalho(txt):
    print(linha())
    print(txt.center(80).upper())
    print(linha())


def banca(API):

	def banca():
		return API.get_balance()

	print(linha())
	print(linha())
	print(''' SUA BANCA: $''',banca())
	print(linha())
	print(linha())

def paridad():
	print('\033[92m',linha())
	par = input(' PARIDADE: ').upper()
	print('\033[92m',linha())

	return par


def Pay(API, par):
	from time import sleep
	API.subscribe_strike_list(par, 1)
	while True:
		d = API.get_digital_current_profit(par, 1)
		if d != False:
			d = round(int(d) / 100, 2)
			break
		sleep(1)
	API.unsubscribe_strike_list(par, 1)
	
	return d

def valores(entrada,stop_l,stop_w,gale_c):
	print('\033[92m',linha())
	valor_entrada = float(entrada) 
	print('Valor de entrada: ',entrada) #float(input(' VALOR INICIAL: '))
	valor_entrada_b = float(valor_entrada)
	print('\033[92m',linha())
	stop_loss = float(stop_l) 
	print('Valor Stop Loss: ',stop_l) #float(input(' STOP LOSS: '))
	print('\033[92m',linha())

	stop_win = float(stop_w) 
	print('Valor Stop Win: ',stop_w) #float(input(' STOP WIN: '))
	print('\033[92m',linha())
	martingale = int(gale_c) 
	print('Quantidade de Martingales: ',gale_c) #int(input(' QUANTOS MARTINGALES? : '))
	martingale += 1
	print('\033[92m',linha())

	return valor_entrada_b, stop_loss, stop_win, martingale
