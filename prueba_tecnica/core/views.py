from django.shortcuts import render, HttpResponse
import requests
import pandas as pd
from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    return HttpResponse("""
    <h1>Ingrese en la URL:</h1>
    <br>
    <h2>/estadisticas-compras/?symbol={symbol}</h2>
    <h2>/estadisticas-ventas/?symbol={symbol}</h2>
    <h2>/estadisticas-generales/</h2>
    <br>
    <p>Corresponde a cada ejercicio con el parametro que indica el simbolo correspondiente</p>
    <p>Ej 2: http://127.0.0.1:8000/estadisticas-compras/?symbol=BTC-USD</p>
    <p>Ej 3: http://127.0.0.1:8000/estadisticas-ventas/?symbol=BTC-USD</p>
    <p>Ej 4: http://127.0.0.1:8000/estadisticas-generales/</p>
    """)

"""
precio (px)
cantidad (qty)
número de órdenes (num)
"""

def estadisticasCompras(request):
    symbol = request.GET.get('symbol')
    response = requests.get(f'https://api.blockchain.com/v3/exchange/l3/{symbol}')
    datos_json = response.json()

    # DataFrame órdenes de compra
    df_bids = pd.DataFrame(datos_json['bids']).fillna(0)

    # El valor medio de las órdenes, donde el valor es la cantidad de la orden multiplicado por su precio.
    value_bids = df_bids['qty'] * df_bids['px']
    average_value = value_bids.mean()

    # greater_value. La orden de compra con mayor valor
    gv_px = df_bids['px'].max()
    gv_qty = df_bids['qty'].max()
    gv_num = df_bids['num'].max()
    gv_value = gv_px * gv_qty

    # lesser_value. La orden de compra con menor valor.
    lv_px = df_bids['px'].min()
    lv_qty = df_bids['qty'].min()
    lv_num = df_bids['num'].min()
    lv_value = lv_px * lv_qty

    # El total de monedas en órdenes.
    total_qty = df_bids['qty'].sum()    

    # El precio total de las órdenes.
    total_px = df_bids['px'].sum()  
    
    greater_value = {}
    greater_value['px'] = str(gv_px)
    greater_value['qty'] = str(gv_qty)
    greater_value['num'] = str(gv_num)
    greater_value['value'] = str(gv_value)
    
    lesser_value = {}
    lesser_value['px'] = str(lv_px)
    lesser_value['qty'] = str(lv_qty)
    lesser_value['num'] = str(lv_num)
    lesser_value['value'] = str(lv_value)

    bids = {}
    bids['average_value'] = average_value
    bids['greater_value'] = greater_value
    bids['lesser_value'] = lesser_value
    bids['total_qty'] = total_qty
    bids['total_px'] = total_px

    datos = {'bids': bids}

    return JsonResponse(datos)

def estadisticasVentas(request):
    symbol = request.GET.get('symbol')
    response = requests.get(f'https://api.blockchain.com/v3/exchange/l3/{symbol}')
    datos_json = response.json()

    # DataFrame órdenes de venta
    df_asks = pd.DataFrame(datos_json['asks']).fillna(0)
    
    # El valor medio de las órdenes, donde el valor es la cantidad de la orden multiplicado por su precio.
    value_asks = df_asks['qty'] * df_asks['px']
    average_value = value_asks.mean() 

    # greater_value. La orden de venta con mayor valor
    gv_px = df_asks['px'].max()
    gv_qty = df_asks['qty'].max()
    gv_num = df_asks['num'].max()
    gv_value = gv_px * gv_qty

    # lesser_value. La orden de venta con menor valor.
    lv_px = df_asks['px'].min()
    lv_qty = df_asks['qty'].min()
    lv_num = df_asks['num'].min()
    lv_value = lv_px * lv_qty

    # El total de monedas en órdenes.
    total_qty = df_asks['qty'].sum()    

    # El precio total de las órdenes.
    total_px = df_asks['px'].sum()  
    
    greater_value = {}
    greater_value['px'] = str(gv_px)
    greater_value['qty'] = str(gv_qty)
    greater_value['num'] = str(gv_num)
    greater_value['value'] = str(gv_value)
    
    lesser_value = {}
    lesser_value['px'] = str(lv_px)
    lesser_value['qty'] = str(lv_qty)
    lesser_value['num'] = str(lv_num)
    lesser_value['value'] = str(lv_value)

    asks = {}
    asks['average_value'] = average_value
    asks['greater_value'] = greater_value
    asks['lesser_value'] = lesser_value
    asks['total_qty'] = total_qty
    asks['total_px'] = total_px

    datos = {'asks': asks}

    return JsonResponse(datos)

def estadisticasGenerales(request):
    response_symbols = requests.get(f'https://api.blockchain.com/v3/exchange/symbols/')
    datos_json_symbol = response_symbols.json()

    # simbolos
    df_symbols = pd.DataFrame(datos_json_symbol)

    datos = []
    
    for symbol in df_symbols:
        response = requests.get(f'https://api.blockchain.com/v3/exchange/l3/{symbol}')
        datos_json = response.json()

        # DataFrame órdenes de compra y venta
        df_bids = pd.DataFrame(datos_json['bids']).fillna(0)
        df_asks = pd.DataFrame(datos_json['asks']).fillna(0)

        try:
            bids_count = len(df_bids)
            bids_qty = df_bids['qty'].sum()
            bids_value = df_asks['px'].sum()     # MONEDA ES SIMBOLO?

            bids = {}
            bids['count'] = str(bids_count)
            bids['qty'] = str(bids_qty)
            bids['value'] = str(bids_value)

        except:
            bids = []

        try:
            asks_count = len(df_asks)
            asks_qty = df_asks['qty'].sum()
            asks_value = df_asks['px'].sum()    # MONEDA ES SIMBOLO?

            asks = {}
            asks['count'] = str(asks_count)
            asks['qty'] = str(asks_qty)
            asks['value'] = str(asks_value)

        except:
            asks = []

        simbolos = {}
        simbolos['bids'] = bids
        simbolos['asks'] = asks

        monedas = {symbol: simbolos}
        datos.append(monedas)

    data = json.dumps(datos)
    return HttpResponse(data)