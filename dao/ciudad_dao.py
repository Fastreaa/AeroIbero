# dao/ciudad_dao.py

from typing import List, Optional
from core.database import get_connection, close_connection


class CiudadDAO:

    @staticmethod
    def get_all() -> List[dict]:
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT id_ciudad, nombre
                FROM ciudad
                ORDER BY nombre
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            close_connection(connection)

    @staticmethod
    def get_by_id(id_ciudad: int) -> Optional[dict]:
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT id_ciudad, nombre
                FROM ciudad
                WHERE id_ciudad = %s
            """
            cursor.execute(query, (id_ciudad,))
            return cursor.fetchone()
        finally:
            close_connection(connection)

    @staticmethod
    def get_by_nombre(nombre: str) -> Optional[dict]:
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT id_ciudad, nombre
                FROM ciudad
                WHERE nombre = %s
            """
            cursor.execute(query, (nombre,))
            return cursor.fetchone()
        finally:
            close_connection(connection)
