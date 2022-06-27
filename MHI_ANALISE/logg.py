def logg ():
	from iqoptionapi.stable_api import IQ_Option
	import sys
	mainUser = {
	'username': "<CONTA>",
	'password': "<SENHA>"
	}
	usuario = mainUser

	API = IQ_Option(usuario["username"], usuario["password"])   

	API.connect()

	API.change_balance('PRACTICE') # PRACTICE / REAL

	if API.check_connect():
		print('\n\nConectado com sucesso')
	else:
		print('\n Erro ao se conectar')
		sys.exit()

	timeframe = 60

	return API, timeframe, usuario