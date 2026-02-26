
# vuelo.py

from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass


class Vuelo:
    """
    Representa un vuelo comercial asociado a una ruta.
    Regla del proyecto: capacidad máxima 20 pasajeros.
    """

    CAPACIDAD_MAXIMA = 20

    def __init__(self,
                 numero_vuelo: str,
                 id_ruta: int,
                 fecha_hora: datetime,
                 id_aeropuerto_origen: int,
                 id_aeropuerto_destino: int,
                 sala: int,
                 puerta: int,
                 capacidad: int = CAPACIDAD_MAXIMA,
                 id_vuelo: Optional[int] = None):

        self.id_vuelo = id_vuelo
        self.numero_vuelo = numero_vuelo.strip().upper()
        self.id_ruta = id_ruta
        self.fecha_hora = fecha_hora
        self.id_aeropuerto_origen = id_aeropuerto_origen
        self.id_aeropuerto_destino = id_aeropuerto_destino
        self.sala = sala
        self.puerta = puerta
        self.capacidad = capacidad

        self._validar_campos()

    def _validar_campos(self):
        if not self.numero_vuelo:
            raise ValueError("numero_vuelo es obligatorio")

        if self.id_ruta <= 0:
            raise ValueError("id_ruta debe ser mayor a 0")

        if not isinstance(self.fecha_hora, datetime):
            raise ValueError("fecha_hora debe ser datetime")

        if self.id_aeropuerto_origen <= 0 or self.id_aeropuerto_destino <= 0:
            raise ValueError("IDs de aeropuerto deben ser mayores a 0")

        if self.id_aeropuerto_origen == self.id_aeropuerto_destino:
            raise ValueError("Origen y destino de aeropuerto no pueden ser iguales")

        if self.sala <= 0 or self.puerta <= 0:
            raise ValueError("sala y puerta deben ser mayores a 0")

        if self.capacidad != self.CAPACIDAD_MAXIMA:
            raise ValueError("La capacidad por vuelo debe ser exactamente 20")

    def hora_abordaje(self) -> datetime:
        return self.fecha_hora - timedelta(minutes=30)

    def esta_programado(self, referencia: Optional[datetime] = None) -> bool:
        ref = referencia or datetime.now()
        return self.fecha_hora > ref

    def to_dict(self) -> dict:
        return {
            "id_vuelo": self.id_vuelo,
            "numero_vuelo": self.numero_vuelo,
            "id_ruta": self.id_ruta,
            "fecha_hora": self.fecha_hora.isoformat(sep=" "),
            "id_aeropuerto_origen": self.id_aeropuerto_origen,
            "id_aeropuerto_destino": self.id_aeropuerto_destino,
            "sala": self.sala,
            "puerta": self.puerta,
            "capacidad": self.capacidad
        }

    def __str__(self):
        return (
            f"Vuelo {self.numero_vuelo} ({self.id_vuelo or 'NUEVO'})\n"
            f"Ruta: {self.id_ruta} | Fecha/Hora: {self.fecha_hora}\n"
            f"Aeropuertos: {self.id_aeropuerto_origen} -> {self.id_aeropuerto_destino}\n"
            f"Sala/Puerta: {self.sala}/{self.puerta} | Capacidad: {self.capacidad}"
        )

    @staticmethod
    def _parse_datetime(valor) -> datetime:
        if isinstance(valor, datetime):
            return valor
        if isinstance(valor, str):
            # Soporta 'YYYY-mm-dd HH:MM:SS' y formato ISO
            try:
                return datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.fromisoformat(valor)
        raise ValueError("No se pudo interpretar fecha_hora")

    @staticmethod
    def from_db_row(row):
        """
        Se espera estructura:
        (id_vuelo, numero_vuelo, id_ruta, fecha_hora, id_aeropuerto_origen,
         id_aeropuerto_destino, sala, puerta, capacidad)
        o dict equivalente.
        """
        if isinstance(row, dict):
            return Vuelo(
                id_vuelo=row.get("id_vuelo"),
                numero_vuelo=row["numero_vuelo"],
                id_ruta=row["id_ruta"],
                fecha_hora=Vuelo._parse_datetime(row["fecha_hora"]),
                id_aeropuerto_origen=row["id_aeropuerto_origen"],
                id_aeropuerto_destino=row["id_aeropuerto_destino"],
                sala=row["sala"],
                puerta=row["puerta"],
                capacidad=row.get("capacidad", Vuelo.CAPACIDAD_MAXIMA)
            )

        (id_vuelo, numero_vuelo, id_ruta, fecha_hora, id_aeropuerto_origen,
         id_aeropuerto_destino, sala, puerta, capacidad) = row
        return Vuelo(
            id_vuelo=id_vuelo,
            numero_vuelo=numero_vuelo,
            id_ruta=id_ruta,
            fecha_hora=Vuelo._parse_datetime(fecha_hora),
            id_aeropuerto_origen=id_aeropuerto_origen,
            id_aeropuerto_destino=id_aeropuerto_destino,
            sala=sala,
            puerta=puerta,
            capacidad=capacidad
        )


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

