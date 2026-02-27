
# pasajero.py

from datetime import date, datetime
from typing import Optional


class Pasajero:
    """
    Representa un pasajero del sistema.
    Incluye validaciones básicas y utilidades para serialización.
    """

    def __init__(self,
                 nombre_completo: str,
                 fecha_nacimiento: date,
                 nacionalidad: str,
                 id_raza: int,
                 telefono: str,
                 correo: str,
                 numero_cliente: Optional[str] = None,
                 id_pasajero: Optional[int] = None):

        self.id_pasajero = id_pasajero
        self.numero_cliente = numero_cliente
        self.nombre_completo = nombre_completo.strip()
        self.fecha_nacimiento = fecha_nacimiento
        self.nacionalidad = nacionalidad.strip()
        self.id_raza = id_raza
        self.telefono = telefono.strip()
        self.correo = correo.strip().lower()

        self._validar_campos()

    def _validar_campos(self):
        if not self.nombre_completo:
            raise ValueError("El nombre completo es obligatorio")

        if not isinstance(self.fecha_nacimiento, date):
            raise ValueError("fecha_nacimiento debe ser date")

        if self.fecha_nacimiento >= date.today():
            raise ValueError("La fecha de nacimiento debe ser anterior al día de hoy")

        if not self.nacionalidad:
            raise ValueError("La nacionalidad es obligatoria")

        if self.id_raza <= 0:
            raise ValueError("id_raza debe ser mayor a 0")

        if not self.telefono:
            raise ValueError("El teléfono es obligatorio")

        if "@" not in self.correo or "." not in self.correo:
            raise ValueError("El correo no tiene un formato válido")

        if self.numero_cliente is not None and not self.numero_cliente.strip():
            raise ValueError("numero_cliente no puede ser cadena vacía")

    def edad(self, referencia: Optional[date] = None) -> int:
        """Calcula la edad del pasajero en años."""
        hoy = referencia or date.today()
        years = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            years -= 1
        return years

    def actualizar_contacto(self,
                            telefono: Optional[str] = None,
                            correo: Optional[str] = None):
        if telefono is not None:
            self.telefono = telefono.strip()
        if correo is not None:
            self.correo = correo.strip().lower()
        self._validar_campos()

    def to_dict(self) -> dict:
        return {
            "id_pasajero": self.id_pasajero,
            "numero_cliente": self.numero_cliente,
            "nombre_completo": self.nombre_completo,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat(),
            "nacionalidad": self.nacionalidad,
            "id_raza": self.id_raza,
            "telefono": self.telefono,
            "correo": self.correo
        }

    def __str__(self):
        return (
            f"Pasajero {self.nombre_completo} ({self.numero_cliente or 'SIN-NUMERO'})\n"
            f"Nacionalidad: {self.nacionalidad}\n"
            f"Edad: {self.edad()} años\n"
            f"Contacto: {self.telefono} | {self.correo}"
        )

    @staticmethod
    def _parse_fecha(fecha_valor) -> date:
        if isinstance(fecha_valor, date):
            return fecha_valor
        if isinstance(fecha_valor, datetime):
            return fecha_valor.date()
        if isinstance(fecha_valor, str):
            return datetime.strptime(fecha_valor, "%Y-%m-%d").date()
        raise ValueError("No se pudo interpretar fecha_nacimiento")

    @staticmethod
    def from_db_row(row):
        """
        Crea un Pasajero desde un registro de BD.
        Soporta tuple/list o dict.
        """
        if isinstance(row, dict):
            return Pasajero(
                id_pasajero=row.get("id_pasajero"),
                numero_cliente=row.get("numero_cliente"),
                nombre_completo=row["nombre_completo"],
                fecha_nacimiento=Pasajero._parse_fecha(row["fecha_nacimiento"]),
                nacionalidad=row["nacionalidad"],
                id_raza=row["id_raza"],
                telefono=row["telefono"],
                correo=row["correo"]
            )

        id_pasajero, numero_cliente, nombre_completo, fecha_nacimiento, nacionalidad, id_raza, telefono, correo = row
        return Pasajero(
            id_pasajero=id_pasajero,
            numero_cliente=numero_cliente,
            nombre_completo=nombre_completo,
            fecha_nacimiento=Pasajero._parse_fecha(fecha_nacimiento),
            nacionalidad=nacionalidad,
            id_raza=id_raza,
            telefono=telefono,
            correo=correo
        )
