# ruta.py

from typing import Optional
from dataclasses import dataclass
from typing import Optional



class Ruta:
    """
    Representa una ruta aérea (grafo dirigido) entre dos ciudades.
    """

    def __init__(self,
                 id_ciudad_origen: int,
                 id_ciudad_destino: int,
                 distancia_km: float,
                 tiempo_total: float,
                 costo_total: float,
                 id_ruta: Optional[int] = None):

        self.id_ruta = id_ruta
        self.id_ciudad_origen = id_ciudad_origen
        self.id_ciudad_destino = id_ciudad_destino
        self.distancia_km = float(distancia_km)
        self.tiempo_total = float(tiempo_total)
        self.costo_total = float(costo_total)

        self._validar_campos()

    def _validar_campos(self):
        if self.id_ciudad_origen <= 0 or self.id_ciudad_destino <= 0:
            raise ValueError("Los IDs de ciudad deben ser mayores a 0")

        if self.id_ciudad_origen == self.id_ciudad_destino:
            raise ValueError("Una ruta no puede tener mismo origen y destino")

        if self.distancia_km <= 0:
            raise ValueError("La distancia debe ser mayor a 0")

        if self.tiempo_total <= 0:
            raise ValueError("El tiempo total debe ser mayor a 0")

        if self.costo_total < 0:
            raise ValueError("El costo total no puede ser negativo")

    def costo_por_km(self) -> float:
        return self.costo_total / self.distancia_km

    def velocidad_promedio_kmh(self) -> float:
        return self.distancia_km / self.tiempo_total

    def to_dict(self) -> dict:
        return {
            "id_ruta": self.id_ruta,
            "id_ciudad_origen": self.id_ciudad_origen,
            "id_ciudad_destino": self.id_ciudad_destino,
            "distancia_km": self.distancia_km,
            "tiempo_total": self.tiempo_total,
            "costo_total": self.costo_total
        }

    def __str__(self):
        return (
            f"Ruta {self.id_ruta or 'NUEVA'}: {self.id_ciudad_origen} -> {self.id_ciudad_destino}\n"
            f"Distancia: {self.distancia_km:.2f} km | Tiempo: {self.tiempo_total:.2f} h | Costo: ${self.costo_total:.2f}"
        )

    @staticmethod
    def from_db_row(row):
        """
        Se espera estructura:
        (id_ruta, id_ciudad_origen, id_ciudad_destino, distancia_km, tiempo_total, costo_total)
        o dict con esas llaves.
        """
        if isinstance(row, dict):
            return Ruta(
                id_ruta=row.get("id_ruta"),
                id_ciudad_origen=row["id_ciudad_origen"],
                id_ciudad_destino=row["id_ciudad_destino"],
                distancia_km=row["distancia_km"],
                tiempo_total=row["tiempo_total"],
                costo_total=row["costo_total"]
            )

        id_ruta, id_ciudad_origen, id_ciudad_destino, distancia_km, tiempo_total, costo_total = row
        return Ruta(
            id_ruta=id_ruta,
            id_ciudad_origen=id_ciudad_origen,
            id_ciudad_destino=id_ciudad_destino,
            distancia_km=distancia_km,
            tiempo_total=tiempo_total,
            costo_total=costo_total
        )

class Ruta:
    id_ruta: Optional[int]
    id_ciudad_origen: int
    id_ciudad_destino: int
    distancia_km: float
    tiempo_total: float
    costo_total: float
