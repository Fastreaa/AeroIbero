from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Pasajero:
    id_pasajero: Optional[int]
    numero_cliente: str
    nombre_completo: str
    fecha_nacimiento: date
    nacionalidad: str
    id_raza: int
    telefono: str
    correo: str
