from dataclasses import dataclass
from typing import Optional


@dataclass
class Ruta:
    id_ruta: Optional[int]
    id_ciudad_origen: int
    id_ciudad_destino: int
    distancia_km: float
    tiempo_total: float
    costo_total: float
