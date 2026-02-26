from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Vuelo:
    id_vuelo: Optional[int]
    numero_vuelo: str
    id_ruta: int
    fecha_hora: datetime
    id_aeropuerto_origen: int
    id_aeropuerto_destino: int
    sala: int
    puerta: int
    capacidad: int = 20
