# dao/reservacion_dao.py

from datetime import timedelta
from typing import List, Optional
from core.database import get_connection, close_connection


class ReservacionDAO:

    @staticmethod
    def crear_reservacion(id_pasajero: int,
                          id_vuelo: int,
                          precio: float) -> Optional[int]:

        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()
            connection.start_transaction()

            # Regla de negocio: máximo 20 pasajeros por vuelo
            capacidad_query = """
                SELECT COUNT(r.id_reservacion)
                FROM reservacion r
                WHERE r.id_vuelo = %s
                FOR UPDATE
            """
            cursor.execute(capacidad_query, (id_vuelo,))
            total_reservados = cursor.fetchone()[0]

            if total_reservados >= 20:
                connection.rollback()
                return None

            cursor.execute("""
                INSERT INTO reservacion (
                    id_pasajero,
                    id_vuelo,
                    precio_pagado
                )
                VALUES (%s, %s, %s)
            """, (id_pasajero, id_vuelo, precio))

            id_reservacion = cursor.lastrowid

            cursor.execute(
                "SELECT fecha_hora FROM vuelo WHERE id_vuelo = %s",
                (id_vuelo,)
            )
            vuelo_fecha = cursor.fetchone()[0]
            hora_abordaje = vuelo_fecha - timedelta(minutes=30)

            cursor.execute("""
                INSERT INTO pase_abordar (
                    id_reservacion,
                    hora_abordaje
                )
                VALUES (%s, %s)
            """, (id_reservacion, hora_abordaje))

            connection.commit()
            return id_reservacion

        except Exception as e:
            connection.rollback()
            print("Error al crear reservación:", e)
            return None

        finally:
            close_connection(connection)

    @staticmethod
    def get_reservas_con_pasajero_y_vuelo() -> List[dict]:
        """
        Devuelve reservaciones con JOIN entre pasajero, reservacion y vuelo.
        """
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT
                    p.id_pasajero,
                    p.numero_cliente,
                    p.nombre_completo,
                    r.id_reservacion,
                    r.precio_pagado,
                    v.id_vuelo,
                    v.numero_vuelo,
                    v.fecha_hora,
                    v.id_ruta
                FROM pasajero p
                JOIN reservacion r ON r.id_pasajero = p.id_pasajero
                JOIN vuelo v ON v.id_vuelo = r.id_vuelo
                ORDER BY v.fecha_hora DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            close_connection(connection)
