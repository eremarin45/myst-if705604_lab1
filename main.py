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
import visualizations as vs
import time
import numpy as np
import pandas as pd
import yfinance as yf
import os
import plotly.graph_objects as go
import plotly.offline as pyo

# data.py
# ------------------------ Paso 1.1
# Obtener lista de archivos a leer
archivos = dt.archivos

# ------------------------ Paso 1.2
# Leer todos los archivos y guardarlos en un diccionario

data_archivos = dt.data_archivos
"""""
# ------------------------ Paso 1.3
# Construir vector de fechas a partir del vector de nombres de archivos

fechas = fn.f_fechas(p_archivos=archivos)

# mostrar las primeras 5 fechas formato 1
print(fechas['i_fechas'][0:4])

# mostrar las primeras 5 fechas formato 1
print(fechas['t_fechas'][0:4])
"""""
