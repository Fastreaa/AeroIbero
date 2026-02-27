# core/servicios.py

import heapq
from math import inf
from typing import Dict, List, Tuple

from dao.ciudad_dao import CiudadDAO
from dao.ruta_dao import RutaDAO


class ServiciosAeroIbero:

    CRITERIOS = {
        "distancia": "distancia_km",
        "tiempo": "tiempo_total",
        "costo": "costo_total"
    }

    @staticmethod
    def _construir_grafo(criterio: str) -> Dict[str, List[Tuple[str, float]]]:
        if criterio not in ServiciosAeroIbero.CRITERIOS:
            raise ValueError("Criterio inválido. Usa: distancia, tiempo o costo")

        ciudades = CiudadDAO.get_all()
        rutas = RutaDAO.get_all()

        if not ciudades:
            return {}

        id_to_nombre = {c["id_ciudad"]: c["nombre"] for c in ciudades}
        peso_key = ServiciosAeroIbero.CRITERIOS[criterio]

        grafo = {nombre: [] for nombre in id_to_nombre.values()}

        for ruta in rutas:
            origen_nombre = id_to_nombre.get(ruta["id_ciudad_origen"])
            destino_nombre = id_to_nombre.get(ruta["id_ciudad_destino"])

            if not origen_nombre or not destino_nombre:
                continue

            peso = float(ruta[peso_key])
            grafo[origen_nombre].append((destino_nombre, peso))

        return grafo

    @staticmethod
    def ejecutar_dijkstra(origen_nombre: str,
                          destino_nombre: str,
                          criterio: str = "distancia") -> dict:

        grafo = ServiciosAeroIbero._construir_grafo(criterio)

        if origen_nombre not in grafo:
            raise ValueError(f"Ciudad de origen inválida: {origen_nombre}")
        if destino_nombre not in grafo:
            raise ValueError(f"Ciudad de destino inválida: {destino_nombre}")

        distancias = {nodo: inf for nodo in grafo}
        anteriores = {nodo: None for nodo in grafo}
        distancias[origen_nombre] = 0.0

        heap = [(0.0, origen_nombre)]

        while heap:
            dist_actual, nodo = heapq.heappop(heap)

            if dist_actual > distancias[nodo]:
                continue

            if nodo == destino_nombre:
                break

            for vecino, peso in grafo[nodo]:
                nueva_distancia = dist_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo
                    heapq.heappush(heap, (nueva_distancia, vecino))

        if distancias[destino_nombre] == inf:
            return {
                "camino": [],
                "costo_total": inf,
                "criterio": criterio,
                "mensaje": "No existe ruta entre las ciudades indicadas"
            }

        camino = []
        actual = destino_nombre
        while actual is not None:
            camino.append(actual)
            actual = anteriores[actual]
        camino.reverse()

        return {
            "camino": camino,
            "costo_total": distancias[destino_nombre],
            "criterio": criterio
        }
