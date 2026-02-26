from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Reservacion:
    id_reservacion: Optional[int]
    id_pasajero: int
    id_vuelo: int
    precio_pagado: float
    fecha_reservacion: Optional[datetime] = None
