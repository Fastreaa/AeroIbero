# dao/pasajero_dao.py

import uuid
from typing import Optional, Dict
from database import get_connection, close_connection
from dao.raza_dao import RazaDAO


class PasajeroDAO:

    # Generar número único de cliente
    @staticmethod
    def generar_numero_cliente() -> str:
        return "CL-" + str(uuid.uuid4())[:8].upper()

    # Insertar pasajero
    @staticmethod
    def insert(nombre_completo: str,
               fecha_nacimiento,
               nacionalidad: str,
               raza: str,
               telefono: str,
               correo: str) -> Optional[int]:

        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()

            #1 Obtener o crear raza
            id_raza = RazaDAO.get_or_create(raza)

            if not id_raza:
                return None

            #2 Generar número cliente
            numero_cliente = PasajeroDAO.generar_numero_cliente()

            query = """
                INSERT INTO pasajero (
                    numero_cliente,
                    nombre_completo,
                    fecha_nacimiento,
                    nacionalidad,
                    id_raza,
                    telefono,
                    correo
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                numero_cliente,
                nombre_completo,
                fecha_nacimiento,
                nacionalidad,
                id_raza,
                telefono,
                correo
            ))

            connection.commit()

            return cursor.lastrowid

        except Exception as e:
            print("Error al insertar pasajero:", e)
            connection.rollback()
            return None

        finally:
            close_connection(connection)

    # Buscar pasajero por ID
    @staticmethod
    def get_by_id(id_pasajero: int) -> Optional[Dict]:

        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT p.*, r.nombre AS raza
                FROM pasajero p
                JOIN raza r ON p.id_raza = r.id_raza
                WHERE p.id_pasajero = %s
            """

            cursor.execute(query, (id_pasajero,))
            return cursor.fetchone()

        finally:
            close_connection(connection)

    # Buscar por número de cliente
    @staticmethod
    def get_by_numero_cliente(numero_cliente: str) -> Optional[Dict]:

        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT p.*, r.nombre AS raza
                FROM pasajero p
                JOIN raza r ON p.id_raza = r.id_raza
                WHERE p.numero_cliente = %s
            """

            cursor.execute(query, (numero_cliente,))
            return cursor.fetchone()

        finally:
            close_connection(connection)
