#./core/servicios.py

from dao.ruta_dao import RutaDAO
from dao.ciudad_dao import CiudadDAO
from algorithms.grafos import Grafo, TablaMapeo
from math import inf


class ServiciosAeroIbero:

    @staticmethod
    def ejecutar_dijkstra(origen_nombre, destino_nombre, criterio="distancia"):

        ciudades = CiudadDAO.get_all()   # Debe devolver id_ciudad y nombre
        rutas = RutaDAO.get_all()

        #  Crear lista de nodos (usaremos nombres)
        nodos = [c["nombre"] for c in ciudades]

        size = len(nodos)

        #  Crear matriz NxN inicializada en 0
        matriz = [[0 for _ in range(size)] for _ in range(size)]

        #  Mapear nombre → índice
        indice = {nodos[i]: i for i in range(size)}

        # Llenar matriz con pesos
        for r in rutas:

            origen_id = r["id_ciudad_origen"]
            destino_id = r["id_ciudad_destino"]

            nombre_origen = next(c["nombre"] for c in ciudades if c["id_ciudad"] == origen_id)
            nombre_destino = next(c["nombre"] for c in ciudades if c["id_ciudad"] == destino_id)

            i = indice[nombre_origen]
            j = indice[nombre_destino]

            if criterio == "distancia":
                peso = float(r["distancia_km"])
            elif criterio == "tiempo":
                peso = float(r["tiempo_total"])
            elif criterio == "costo":
                peso = float(r["costo_total"])
            else:
                raise ValueError("Criterio inválido")

            matriz[i][j] = peso

        # Crear grafo con tu clase original
        grafo = Grafo(nodos, matriz)
        tabla = TablaMapeo(grafo)

        # Ejecutar Dijkstra
        tabla.dijkstra(origen_nombre)

        # Obtener camino
        camino = tabla.findPath(destino_nombre)

        nodo_destino = tabla.findNodo(destino_nombre)

        return {
            "camino": camino,
            "costo_total": nodo_destino.costo
        }
