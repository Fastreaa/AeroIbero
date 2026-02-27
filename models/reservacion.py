# reservacion.py
from datetime import datetime
from typing import Optional


class Reservacion:
    """
    Representa una reservación de un pasajero para un vuelo.
    """

    def __init__(self,
                 id_pasajero: int,
                 id_vuelo: int,
                 precio_pagado: float,
                 id_reservacion: Optional[int] = None,
                 fecha_reservacion: Optional[datetime] = None):

        self.id_reservacion = id_reservacion
        self.id_pasajero = id_pasajero
        self.id_vuelo = id_vuelo
        self.precio_pagado = float(precio_pagado)
        self.fecha_reservacion = fecha_reservacion or datetime.now()

        self._validar_campos()

    def _validar_campos(self):
        if self.id_pasajero <= 0:
            raise ValueError("id_pasajero debe ser mayor a 0")

        if self.id_vuelo <= 0:
            raise ValueError("id_vuelo debe ser mayor a 0")

        if self.precio_pagado < 0:
            raise ValueError("precio_pagado no puede ser negativo")

        if not isinstance(self.fecha_reservacion, datetime):
            raise ValueError("fecha_reservacion debe ser datetime")

    def actualizar_precio(self, nuevo_precio: float):
        self.precio_pagado = float(nuevo_precio)
        self._validar_campos()

    def to_dict(self) -> dict:
        return {
            "id_reservacion": self.id_reservacion,
            "id_pasajero": self.id_pasajero,
            "id_vuelo": self.id_vuelo,
            "precio_pagado": self.precio_pagado,
            "fecha_reservacion": self.fecha_reservacion.isoformat(sep=" ")
        }

    def __str__(self):
        return (
            f"Reservación {self.id_reservacion or 'NUEVA'}\n"
            f"Pasajero: {self.id_pasajero} | Vuelo: {self.id_vuelo}\n"
            f"Precio pagado: ${self.precio_pagado:.2f}\n"
            f"Fecha reservación: {self.fecha_reservacion}"
        )

    @staticmethod
    def _parse_datetime(valor) -> datetime:
        if isinstance(valor, datetime):
            return valor
        if isinstance(valor, str):
            try:
                return datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.fromisoformat(valor)
        raise ValueError("No se pudo interpretar fecha_reservacion")

    @staticmethod
    def from_db_row(row):
        """
        Se espera estructura:
        (id_reservacion, id_pasajero, id_vuelo, precio_pagado, fecha_reservacion)
        o dict equivalente.
        """
        if isinstance(row, dict):
            return Reservacion(
                id_reservacion=row.get("id_reservacion"),
                id_pasajero=row["id_pasajero"],
                id_vuelo=row["id_vuelo"],
                precio_pagado=row["precio_pagado"],
                fecha_reservacion=Reservacion._parse_datetime(
                    row.get("fecha_reservacion", datetime.now())
                )
            )

        id_reservacion, id_pasajero, id_vuelo, precio_pagado, fecha_reservacion = row
        return Reservacion(
            id_reservacion=id_reservacion,
            id_pasajero=id_pasajero,
            id_vuelo=id_vuelo,
            precio_pagado=precio_pagado,
            fecha_reservacion=Reservacion._parse_datetime(fecha_reservacion)
        )

