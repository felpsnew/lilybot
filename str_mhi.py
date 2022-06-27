def mhivdd(API, par, tipo_mhi):    
    import time
    from iqoptionapi.stable_api import IQ_Option
    from datetime import datetime

    minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
    entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False

    dir = ''
    if entrar:

        velas = API.get_candles(par, 60, 3, time.time())
        
        velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
        velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
        velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
        
        cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]        
    
        if cores.count('g') > cores.count('r') and cores.count('d') == 0 : dir = ('put' if tipo_mhi == 1 else 'call')
        print('\n\nMHI Call')

        if cores.count('r') > cores.count('g') and cores.count('d') == 0 : dir = ('call' if tipo_mhi == 1 else 'put')

        if dir == 'call':
            print('\n\nMHI Call')
        if dir == 'put':
            print('\n\nMHI Put')

    return dir


def mhiGale(API, par, tipo_mhi = 2):    
    import time
    from iqoptionapi.stable_api import IQ_Option
    from datetime import datetime

    dir = ''

    velas = API.get_candles(par, 60, 3, time.time())
    
    velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
    velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
    velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
    
    cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]        

    if cores.count('g') > cores.count('r') and cores.count('d') == 0 : dir = ('put' if tipo_mhi == 1 else 'call')

    if cores.count('r') > cores.count('g') and cores.count('d') == 0 : dir = ('call' if tipo_mhi == 1 else 'put')

    # if dir == 'call':
    #     print('\n\nMHI Call')
    # if dir == 'put':
    #     print('\n\nMHI Put')

    return dir

    
    
