# dao/aeropuerto_dao.py

from typing import List, Optional
from database import get_connection, close_connection
from models.aeropuerto import Aeropuerto


class AeropuertoDAO:

    # Obtener aeropuerto por ID
    @staticmethod
    def get_by_id(id_aeropuerto: int) -> Optional[Aeropuerto]:
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()

            query = """
                SELECT 
                    c.nombre AS ciudad,
                    p.nombre AS pais,
                    a.nombre AS aeropuerto,
                    c.tipo,
                    a.total_salas,
                    a.total_puertas
                FROM aeropuerto a
                JOIN ciudad c ON a.id_ciudad = c.id_ciudad
                JOIN pais p ON c.id_pais = p.id_pais
                WHERE a.id_aeropuerto = %s
            """
            cursor.execute(query, (id_aeropuerto,))
            row = cursor.fetchone()

            if row:
                return Aeropuerto.from_db_row(row)

            return None

        finally:
            close_connection(connection)

    # Obtener aeropuerto por nombre
    @staticmethod
    def get_by_nombre(nombre: str) -> Optional[Aeropuerto]:
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()

            query = """
                SELECT 
                    c.nombre AS ciudad,
                    p.nombre AS pais,
                    a.nombre AS aeropuerto,
                    c.tipo,
                    a.total_salas,
                    a.total_puertas
                FROM aeropuerto a
                JOIN ciudad c ON a.id_ciudad = c.id_ciudad
                JOIN pais p ON c.id_pais = p.id_pais
                WHERE a.nombre = %s
            """

            cursor.execute(query, (nombre,))
            row = cursor.fetchone()

            if row:
                return Aeropuerto.from_db_row(row)

            return None

        finally:
            close_connection(connection)

    # Obtener todos los aeropuertos
    @staticmethod
    def get_all() -> List[Aeropuerto]:
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor()

            query = """
                SELECT 
                    c.nombre AS ciudad,
                    p.nombre AS pais,
                    a.nombre AS aeropuerto,
                    c.tipo,
                    a.total_salas,
                    a.total_puertas
                FROM aeropuerto a
                JOIN ciudad c ON a.id_ciudad = c.id_ciudad
                JOIN pais p ON c.id_pais = p.id_pais
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            return [Aeropuerto.from_db_row(row) for row in rows]

        finally:
            close_connection(connection)

    # Insertar aeropuerto nuevo
    @staticmethod
    def insert(nombre: str, id_ciudad: int, total_salas: int, total_puertas: int) -> bool:
        connection = get_connection()
        if not connection:
            return False

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO aeropuerto (nombre, id_ciudad, total_salas, total_puertas)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (nombre, id_ciudad, total_salas, total_puertas))
            connection.commit()

            return True

        except Exception as e:
            print("Error al insertar aeropuerto:", e)
            connection.rollback()
            return False

        finally:
            close_connection(connection)

    # Eliminar aeropuerto
    @staticmethod
    def delete(id_aeropuerto: int) -> bool:
        connection = get_connection()
        if not connection:
            return False

        try:
            cursor = connection.cursor()

            query = "DELETE FROM aeropuerto WHERE id_aeropuerto = %s"
            cursor.execute(query, (id_aeropuerto,))
            connection.commit()

            return True

        except Exception as e:
            print("Error al eliminar aeropuerto:", e)
            connection.rollback()
            return False

        finally:
            close_connection(connection)
