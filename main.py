"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import data as dt
import functions as fn
import numpy as np
import pandas as pd
import yfinance as yf
import os

# ------------------------ Paso 1.1
# Obtener lista de archivos a leer
archivos = dt.archivos

# ------------------------ Paso 1.2
# Leer todos los archivos y guardarlos en un diccionario
data_archivos = dt.data_archivos

# ------------------------ Paso 1.3
# Construir vector de fechas a partir del vector de nombres de archivos
fechas = fn.fechas_i(archivos)
diario = pd.date_range(start=fn.fechas_i(archivos)[0], end=fn.fechas_i(archivos)[-1])
diario = diario.strftime('%Y-%m-%d')

# formato 2
fechas = fn.fechas_j(archivos)
diario = pd.date_range(start=fn.fechas_j(archivos)[0], end=fn.fechas_j(archivos)[-1])
diario = diario.strftime('%Y-%m-%d')

# mostrar las primeras 5 fechas formato 1
print(fechas['fechas_i'][0:4])

# mostrar las primeras 5 fechas formato 2
print(fechas['fechas_j'][0:4])

# ------------------------ Paso 1.4
#  Construir el vector de tickers que vamos a utilizar en yfinance
tickers = fn.global_tickers(archivos)

# ------------------------ Paso 1.5
# Descargar y acomodar todos los precios historicos
precios = fn.preciosyf(archivos)
precio_c = fn.preciosyf[0]

# ------------------------ Paso 1.6
# inversion pasiva
k = 1000000
c = 0.00125
# Peso
# Obtener el rendimiento en cada periodo
# grafica

#  ------------------------ Paso 1.6
# inversion activa
# obtener sharpe
# realizar balanceos
# grafica
