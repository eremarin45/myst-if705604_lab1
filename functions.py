"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import os
import yfinance as yf
import numpy as np


# fechas de los archivos
def fechas_i(archivos):
    t_fechas = [i.strftime("%d-%m-%Y") for i in sorted(pd.to_datetime(i[8:]).date() for i in archivos)]
    return t_fechas


# lista con fechas ordenadas (para usarse como indexadores de archivos)
def fechas_j(archivos):
    i_fechas = [j.strftime("%d%m%Y") for j in sorted(pd.to_datetime(i[8:]).date() for i in archivos)]
    return i_fechas


# func para los tickers compatibles yfinance
def global_tickers(archivos, data_archivos):
    tickers = []

    for i in archivos:
        l_ticker = list(data_archivos[i]["Ticker"])
        [tickers.append(i + ".MX") for i in l_ticker]

    global_tickers = np.unique(tickers).tolist()
    # eliminar MXN, USD, y tickers con problemas de precios: KOFL, BSMXB
    [global_tickers.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'BSMXB.MX']]

    # ajustes de nombre de tickers
    global_tickers = [i.replace("GFREGIOO.MX", "RA.MX") for i in global_tickers]
    global_tickers = [i.replace("MEXCHEM.MX", "ORBIA.MX") for i in global_tickers]
    global_tickers = [i.replace("LIVEPOLC.1.MX", "LIVEPOLC-1.MX") for i in global_tickers]

    return global_tickers

# Descargar precios Yfinance
def preciosyf(archivos):
    data = yf.download(global_tickers, start="2017-08-21", end="2020-08-22", actions=False,
                       group_by="close", interval="1d", auto_adjust=True, prepost=False, threads=True)
    # Mostrar precio cierre
    close = pd.DataFrame({i: data[i]['Close'] for i in global_tickers(archivos)})
    return close

# inv pasiva
def inv_pasiva(archivos, fechas_i, k, c, inv_pasiva):
    # activos
    activos = list(dt.data_archivos[list(dt.data_archivos['Ticker'].isin(dt.data_archivos))].index)
