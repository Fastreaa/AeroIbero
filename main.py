import pandas as pd
from math import inf

# Leer el archivo
vuelos = pd.read_csv('./Ciudades_Aeroibero.csv')

# Obtener todos loas puntos de origen y de destino
origenes = vuelos['Origen'].unique()
destinos = vuelos['Destino'].unique()

missing_origenes = []
missing_destinos = []

# Obtener los puntos que son mencionados en una columna pero no en la otra para agregarlos
for origen in origenes:
    if origen not in destinos:
        missing_destinos.append(origen)
        vuelos.loc[len(vuelos)] = [origen, origen, None, inf, inf, inf]

for destino in destinos:
    if destino not in origenes:
        missing_origenes.append(destino)
        vuelos.loc[len(vuelos)] = [destino, destino, None, inf, inf, inf]

# Crea 3 matrices de origenes y destinos considerando la distancia, el tiempo y el costo
# Las acomoda para tener la forma de una matriz de adyacencia
# Esto genera 3 matrices de adyacencia en una, con 3 diferentes costos: distancia, tiempo y precio listas para operarse con Djikstra
matrix = vuelos.pivot(index='Origen', columns='Destino', values=['Distancia (Km)', 'Tiempo total (Hrs)', 'Costo total']).sort_index()
matrix.fillna(inf, inplace=True)