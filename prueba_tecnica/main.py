import requests
import sys
import os
import pandas as pd
import psycopg2
from sqlalchemy import *
from prueba_tecnica.settings import DATABASES

symbol = sys.argv[1]
dir = 'output'

# Config database settings.py Django
bbdd_name = DATABASES['default']['NAME']
bbdd_user = DATABASES['default']['USER']
bbdd_pass = DATABASES['default']['PASSWORD']
bbdd_host = DATABASES['default']['HOST']
bbdd_port = DATABASES['default']['PORT']

def check_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)

if __name__ == '__main__':

    # requests GET to JSON
    response = requests.get(f'https://api.blockchain.com/v3/exchange/l3/{symbol}')
    datos_json = response.json()
    
    df_bids = pd.DataFrame(datos_json['bids'])      # órdenes de compra
    df_asks = pd.DataFrame(datos_json['asks'])      # órdenes de venta

    # save .csv
    check_dir(dir)
    df_bids.to_csv(f'{dir}/bids_{symbol}.csv', sep=';', index=False)
    df_asks.to_csv(f'{dir}/asks_{symbol}.csv', sep=';', index=False)

    # save postgresql
    bbdd_prueba = create_engine(f'postgresql+psycopg2://{bbdd_user}:{bbdd_pass}@{bbdd_host}:{bbdd_port}/{bbdd_name}')
    conection = bbdd_prueba.connect()

    df_bids.to_sql('bbdd_bids', bbdd_prueba, if_exists='append', index=False)
    df_asks.to_sql('bbdd_asks', bbdd_prueba, if_exists='append', index=False)

    conection.close()
