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
                SELECT id_ciudad, id_pais, nombre, tipo
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

                SELECT id_ciudad, id_pais, nombre, tipo
                FROM ciudad
                WHERE nombre = %s
            """
            cursor.execute(query, (nombre.strip(),))
            return cursor.fetchone()
        finally:
            close_connection(connection)

    @staticmethod
    def get_by_pais(id_pais: int) -> List[dict]:
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT id_ciudad, id_pais, nombre, tipo
                FROM ciudad
                WHERE id_pais = %s
                ORDER BY nombre
            """
            cursor.execute(query, (id_pais,))
            return cursor.fetchall()
        finally:
            close_connection(connection)

    @staticmethod
    def insert(id_pais: int, nombre: str, tipo: str) -> Optional[int]:
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO ciudad (id_pais, nombre, tipo)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (id_pais, nombre.strip(), tipo.strip()))
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al insertar ciudad:", e)
            connection.rollback()
            return None
        finally:
            close_connection(connection)

    @staticmethod
    def update(id_ciudad: int,
               id_pais: Optional[int] = None,
               nombre: Optional[str] = None,
               tipo: Optional[str] = None) -> bool:
        connection = get_connection()
        if not connection:
            return False

        try:
            campos = []
            valores = []

            if id_pais is not None:
                campos.append("id_pais = %s")
                valores.append(id_pais)

            if nombre is not None:
                campos.append("nombre = %s")
                valores.append(nombre.strip())

            if tipo is not None:
                campos.append("tipo = %s")
                valores.append(tipo.strip())

            if not campos:
                return False

            query = f"UPDATE ciudad SET {', '.join(campos)} WHERE id_ciudad = %s"
            valores.append(id_ciudad)

            cursor = connection.cursor()
            cursor.execute(query, tuple(valores))
            connection.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print("Error al actualizar ciudad:", e)
            connection.rollback()
            return False
        finally:
            close_connection(connection)

    @staticmethod
    def delete(id_ciudad: int) -> bool:
        connection = get_connection()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            query = "DELETE FROM ciudad WHERE id_ciudad = %s"
            cursor.execute(query, (id_ciudad,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al eliminar ciudad:", e)
            connection.rollback()
            return False
        finally:
            close_connection(connection)

