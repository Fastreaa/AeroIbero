
# pase_abordar.py


from dataclasses import dataclass
from datetime import datetime
from typing import Optional



class PaseAbordar:
    """
    Representa un pase de abordar asociado a una reservación.
    """

    def __init__(self,
                 id_reservacion: int,
                 hora_abordaje: datetime,
                 qr_data: Optional[str] = None,
                 id_pase: Optional[int] = None):

        self.id_pase = id_pase
        self.id_reservacion = id_reservacion
        self.hora_abordaje = hora_abordaje
        self.qr_data = qr_data

        self._validar_campos()

    def _validar_campos(self):
        if self.id_reservacion <= 0:
            raise ValueError("id_reservacion debe ser mayor a 0")

        if not isinstance(self.hora_abordaje, datetime):
            raise ValueError("hora_abordaje debe ser datetime")

        if self.qr_data is not None and not self.qr_data.strip():
            raise ValueError("qr_data no puede estar vacío")

    def set_qr_data(self, data: str):
        self.qr_data = data.strip()
        self._validar_campos()

    def to_dict(self) -> dict:
        return {
            "id_pase": self.id_pase,
            "id_reservacion": self.id_reservacion,
            "hora_abordaje": self.hora_abordaje.isoformat(sep=" "),
            "qr_data": self.qr_data
        }

    def __str__(self):
        return (
            f"Pase {self.id_pase or 'NUEVO'}\n"
            f"Reservación: {self.id_reservacion}\n"
            f"Hora de abordaje: {self.hora_abordaje}\n"
            f"QR: {'CARGADO' if self.qr_data else 'PENDIENTE'}"
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
        raise ValueError("No se pudo interpretar hora_abordaje")

    @staticmethod
    def from_db_row(row):
        """
        Se espera estructura:
        (id_pase, id_reservacion, hora_abordaje, qr_data)
        o dict equivalente.
        """
        if isinstance(row, dict):
            return PaseAbordar(
                id_pase=row.get("id_pase"),
                id_reservacion=row["id_reservacion"],
                hora_abordaje=PaseAbordar._parse_datetime(row["hora_abordaje"]),
                qr_data=row.get("qr_data")
            )

        id_pase, id_reservacion, hora_abordaje, qr_data = row
        return PaseAbordar(
            id_pase=id_pase,
            id_reservacion=id_reservacion,
            hora_abordaje=PaseAbordar._parse_datetime(hora_abordaje),
            qr_data=qr_data
        )
@dataclass
class PaseAbordar:
    id_pase: Optional[int]
    id_reservacion: int
    hora_abordaje: datetime
    qr_data: Optional[str] = None
