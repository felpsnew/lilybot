import linecache 


valor_entrada_b = linecache.getline('config.txt',7)
stop_loss = linecache.getline('config.txt',8)
stop_win = linecache.getline('config.txt',9)
martingale = linecache.getline('config.txt',10)

print(valor_entrada_b,stop_loss,stop_win,martingale)