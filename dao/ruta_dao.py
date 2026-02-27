# dao/ruta_dao.py

from typing import List, Optional
from core.database import get_connection, close_connection


class RutaDAO:

    @staticmethod
    def get_all() -> List[dict]:
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT
                    id_ruta,
                    id_ciudad_origen,
                    id_ciudad_destino,
                    distancia_km,
                    tiempo_total,
                    costo_total
                FROM ruta
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            close_connection(connection)

    @staticmethod
    def get_by_id(id_ruta: int) -> Optional[dict]:
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT
                    id_ruta,
                    id_ciudad_origen,
                    id_ciudad_destino,
                    distancia_km,
                    tiempo_total,
                    costo_total
                FROM ruta
                WHERE id_ruta = %s
            """
            cursor.execute(query, (id_ruta,))
            return cursor.fetchone()
        finally:
            close_connection(connection)

    @staticmethod
    def insert(id_ciudad_origen: int,
               id_ciudad_destino: int,
               distancia_km: float,
               tiempo_total: float,
               costo_total: float) -> Optional[int]:
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO ruta (
                    id_ciudad_origen,
                    id_ciudad_destino,
                    distancia_km,
                    tiempo_total,
                    costo_total
                )
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                id_ciudad_origen,
                id_ciudad_destino,
                distancia_km,
                tiempo_total,
                costo_total
            ))
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al insertar ruta:", e)
            connection.rollback()
            return None
        finally:
            close_connection(connection)
