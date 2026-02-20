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
    """

    def __init__(self, ciudad: str, pais: str, nombre: str, tipo: TipoCiudad):
        self.ciudad = ciudad
        self.pais = pais
        self.nombre = nombre
        self.tipo = tipo

        # Según el proyecto:
        # Ordinaria -> al menos 1 sala y 1 puerta
        # Importante / Preguntar mañana / Capital -> al menos 3 salas y 3 puertas
        if tipo == TipoCiudad.ORDINARIA:
            self.total_salas = 1
            self.total_puertas = 1
        else:
            self.total_salas = 3
            self.total_puertas = 3

        # Estado interno
        self.salas_disponibles = set(range(1, self.total_salas + 1))
        self.puertas_disponibles = set(range(1, self.total_puertas + 1))


    def asignar_sala(self) -> Optional[int]:
        """Asigna una sala disponible si existe."""
        if not self.salas_disponibles:
            return None

        sala = self.salas_disponibles.pop()
        return sala

    def asignar_puerta(self) -> Optional[int]:
        """Asigna una puerta disponible si existe."""
        if not self.puertas_disponibles:
            return None

        puerta = self.puertas_disponibles.pop()
        return puerta

    def liberar_sala(self, numero: int):
        """Libera una sala previamente asignada."""
        if 1 <= numero <= self.total_salas:
            self.salas_disponibles.add(numero)

    def liberar_puerta(self, numero: int):
        """Libera una puerta previamente asignada."""
        if 1 <= numero <= self.total_puertas:
            self.puertas_disponibles.add(numero)

    #Info del aeropuerto

    def es_internacional(self) -> bool:
        """Retorna True si el aeropuerto puede manejar vuelos internacionales."""
        return self.tipo in {TipoCiudad.IMPORTANTE, TipoCiudad.CAPITAL}

    def info(self) -> dict:
        """Devuelve información estructurada del aeropuerto."""
        return {
            "ciudad": self.ciudad,
            "pais": self.pais,
            "nombre": self.nombre,
            "tipo": self.tipo.value,
            "salas_totales": self.total_salas,
            "puertas_totales": self.total_puertas,
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
        