# aeropuerto.py


from enum import Enum
from typing import Optional


class TipoCiudad(Enum):
    ORDINARIA = "Ordinaria"
    IMPORTANTE = "Importante"
    CAPITAL = "Capital"


class Aeropuerto:
    """
    Representa un aeropuerto dentro del sistema Aero-Ibero.
    Este objeto modela un aeropuerto almacenado en la base de datos.
    """

    def __init__(self, ciudad: str, pais: str, nombre: str, tipo: TipoCiudad,
                 total_salas: Optional[int] = None,
                 total_puertas: Optional[int] = None):

        self.ciudad = ciudad
        self.pais = pais
        self.nombre = nombre
        self.tipo = tipo

        # Si vienen de la BD, usar esos valores.
        # Si no, calcular según reglas del proyecto.
        if total_salas is not None and total_puertas is not None:
            self.total_salas = total_salas
            self.total_puertas = total_puertas
        else:
            if tipo == TipoCiudad.ORDINARIA:
                self.total_salas = 1
                self.total_puertas = 1
            else:
                self.total_salas = 3
                self.total_puertas = 3

        # Estado dinámico en memoria
        self.salas_disponibles = set(range(1, self.total_salas + 1))
        self.puertas_disponibles = set(range(1, self.total_puertas + 1))

    # Métodos de asignación

    def asignar_sala(self) -> Optional[int]:
        """Asigna una sala disponible si existe."""
        if not self.salas_disponibles:
            return None
        return self.salas_disponibles.pop()

    def asignar_puerta(self) -> Optional[int]:
        """Asigna una puerta disponible si existe."""
        if not self.puertas_disponibles:
            return None
        return self.puertas_disponibles.pop()

    def liberar_sala(self, numero: int):
        """Libera una sala previamente asignada."""
        if 1 <= numero <= self.total_salas:
            self.salas_disponibles.add(numero)

    def liberar_puerta(self, numero: int):
        """Libera una puerta previamente asignada."""
        if 1 <= numero <= self.total_puertas:
            self.puertas_disponibles.add(numero)

    # Información del aeropuerto

    def es_internacional(self) -> bool:
        """Retorna True si el aeropuerto puede manejar vuelos internacionales."""
        return self.tipo in {TipoCiudad.IMPORTANTE, TipoCiudad.CAPITAL}

    def to_dict(self) -> dict:
        """Devuelve representación estructurada del aeropuerto."""
        return {
            "ciudad": self.ciudad,
            "pais": self.pais,
            "nombre": self.nombre,
            "tipo": self.tipo.value,
            "total_salas": self.total_salas,
            "total_puertas": self.total_puertas,
            "salas_disponibles": len(self.salas_disponibles),
            "puertas_disponibles": len(self.puertas_disponibles)
        }

    def __str__(self):
        return (
            f"Aeropuerto {self.nombre} ({self.ciudad}, {self.pais})\n"
            f"Tipo: {self.tipo.value}\n"
            f"Salas disponibles: {len(self.salas_disponibles)}/{self.total_salas}\n"
            f"Puertas disponibles: {len(self.puertas_disponibles)}/{self.total_puertas}"
        )
-
    # Método de fábrica para crear desde BD

    @staticmethod
    def from_db_row(row: tuple):
        """
        Crea un objeto Aeropuerto a partir de un registro de la BD.
        Se espera que row tenga:
        (ciudad, pais, nombre, tipo, total_salas, total_puertas)
        """

        ciudad, pais, nombre, tipo_str, total_salas, total_puertas = row

        tipo = TipoCiudad(tipo_str)

        return Aeropuerto(
            ciudad=ciudad,
            pais=pais,
            nombre=nombre,
            tipo=tipo,
            total_salas=total_salas,
            total_puertas=total_puertas
        )
