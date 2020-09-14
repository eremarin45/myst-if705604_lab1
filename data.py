"""
# Proceso de adquisicion de datos
# Si se vuelve funcion, pasar a functions
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
from datetime import datetime
from os import path, listdir
from os.path import isfile, join
import numpy as np
import time
import yfinance as yf

pd.set_option("display.max_rows", None)  # sin limite de renglones max
pd.set_option("display.max_columns", None)  # " " col max
pd.set_option("display.width", None)  # " " ancho del display
pd.set_option("display.expand_frame_repr", None)  # visualizar todas las col

# ----------------------------------------------------------------------- Paso 1.1
# --obtener lista de los archivos a leer

# obtener ruta de los archivos por carpeta
abspath = path.abspath('files/NAFTRAC_holdings')

# obtener lista de los archivos de la carpeta sin la extension
archivos = [f[:-4] for f in listdir(abspath) if isfile(join(abspath, f))]

# ----------- leer todos los archivos y guardarlos en un diccionario ---- Paso 1.2
# Crear diccionario {} para todos los archivos
data_archivos = {}
# pd.read_csv('files/NAFTRAC_holdings_210820.csv', skiprows=2, header=None)
archivos = sorted(archivos, key=lambda t: datetime.strptime(t[8:], '%d%m%y'))

for i in archivos:
    # Leer los archivos despues de 2 renglones sin info
    data = pd.read_csv('files/NAFTRAC_holdings/' + i + '.csv', skiprows=2, header=None)

    # renombrar columnas con lo que tiene el 1er renglon
    data.columns = list(data.iloc[0, :])
    # quitar columnas que no sean null
    data = data.loc[:, pd.notnull(data.columns)]
    # resetear el indice
    data = data.iloc[1:-1].reset_index(drop=True, inplace=False)
    # quitar las comas en la col de precios
    data['Precio'] = [i.replace(',', ' ') for i in data['Precio']]
    # Quitar asterisco al Ticker
    data['Ticker'] = [i.replace('*', ' ') for i in data['Ticker']]
    # Convretir a numerico
    convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
    data = data.astype(convert_dict, errors='ignore')
    # Convertir a decimal col de peso %
    data['Peso (%)'] = data['Peso (%)']/100
    # Guardar en diccionario
    data_archivos[i] = data

# --- Construir vector de fechas a partir del vector de nombres de archivos------- Paso 1.3
# Estas serviran como etiqueta en data frame y yahoo finance
t_fechas = [i.strftime('%d-%m-%Y') for i in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

# Lista con fechas ordenadas (para usar como indexador de archivos)
i_fechas = [j.strftime('%d-%m-%Y') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

# -------- Construir el vector de tickers que vamos a utilizar en yfinance --- Paso 1.4
tickers = []
for i in archivos:
    # i = archivos[1] checar si funciona
    l_tickers = list(data_archivos[i]['Ticker'])
    [tickers.append(i + '.MX') for i in l_tickers]

global_tickers = np.unique(tickers).tolist()
# eliminar MXN, USD, y tickers con problemas de precios: KOFL, BSMXB
[global_tickers.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'BSMXB.MX']]

# -------- Descargar y acomodar todos los precios historicos --- Paso 1.5
# cambios en nombres de tickers
global_tickers = [i.replace('GFREGIO.MX', 'RA.MX') for i in global_tickers]
global_tickers = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_tickers]
global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]

# contar tiempo
inicio = time.time()

# descarga  de precios de yfinance
data = yf.download(global_tickers, start="2017-08-21", end="2020-08-21", actions=False,
                   group_by="close", interval='1d', auto_adjust=True, prepost=False, threads=True)

# time
print('se tardo', round(time.time() - inicio, 2), 'segundos')

# ------- Obtener posiciones historicas ---------------------------- Paso 1.6
# nota, pasar en todos los meses las posiciones en KOFL.MXN y BSMXB.MX a CASH en MXN
close = pd.DataFrame({i: data[i]["Close"] for i in global_tickers})

# tomar solo fechas de interes
fechas = [j.strftime("%Y-%m-%d") for j in sorted(pd.to_datetime(i[8:]).date() for i in archivos)]
# Se cambia el tipo de fecha para que se ajuste al mismo formato y veamos si se encuentran todas
ic_fechas = sorted(list(set(close.index.astype(str).tolist()) & set(fechas)))
# Localizar todos los precios
precios = np.concatenate([np.where(close.index == ic_fechas[i]) for i in range(len(ic_fechas))])\
    .reshape(len(ic_fechas),)
# Elegir Posiciones históricas
closes_timeframe = close.iloc[precios, :]

# Ordenar columnas en orden lexográfico
precios = closes_timeframe.reindex(sorted(closes_timeframe.columns), axis=1)


# transponer matriz para tener x: fechas y: precios
# multiplicar matriz de precios por matriz de pesos
# hacer suma de cada col para obtener valor marcado
"""""
# Posicion inicial
k = 1000000 # capital inicial
c = 0.00125 # comisiones por transaccion

# Vector de comisiones historicas
comisiones = []

# Obtener posicion inicial
# los % para KOFL, KOFUBL, BSMXB, USD asignarlos a CASH
c_activos = ['KOFL', 'KOFUBL', 'BSMXB', 'MXN', 'USD']

data_archivos[archivos[0]]['Peso (%)']*(k//data_archivos[archivos[0]]['Peso (%)'])


# Diccionario para resultado final
inv_pasiva = {'timestamp': ['05-01-2018'], 'capital': [k]}

data_archivos[archivos[0]].copy().sort_values('Ticker').isin(c_activos)

pos_datos = data_archivos[archivos[0]].copy().sort_values('Ticker')[['Ticker', 'Nombre', 'Peso (%)']]

# extraer la lista de activos a eliminar
i_activos = list(pos_datos[pos_datos['Ticker'].isin(c_activos)].index)

# eliminar los activos del dataframe
pos_datos.drop(i_activos, inplace=True)
# resetear el index
pos_datos.reset_index(inplace=True, drop=True)

# agregar .MX para empatar precios
pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'

# Corregir tickers en datos
pos_datos['Ticker'] = pos_datos['Ticker'].replace('LIVERPOLC.1.MX', 'LIVERPOL-1.MX')
pos_datos['Ticker'] = pos_datos['Ticker'].replace('MEXCHEM.MX', 'ORBIA.MX')
pos_datos['Ticker'] = pos_datos['Ticker'].replace('GFREGIOO.MX', 'RA.MX')


# Desgloce
# fecha en la que busca hacer el match de precios
match = 7
precios.index.to_list()[match]

# precios necesarios para la posicion metodo 1
m1 = np.array(precios.iloc[match, [i in pos_datos['Ticker'].to_list() for i in precios.columns.to_list()]])
m2 = [precios.iloc[match, precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]

pos_datos['Precio_m1'] = m1
pos_datos['Precio_m2'] = m2

pos_datos['Precio'] = np.array(precios.iloc[0, (i in pos_datos['Ticker'].to.list() for i in
#                                             precios.columns.to_list())])

# Capital destinado por accion = proporcion de capital - comisiones por la posicion
pos_datos['Capital'] = pos_datos['Peso (%)'] * k - pos_datos['Peso (%)'] * k * c

# Cantidad de titulos por acción
pos_datos['Titulos'] = pos_datos['Capital'] // pos_datos['Precio']
"""