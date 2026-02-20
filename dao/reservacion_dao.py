# reservacion_dao.py

@staticmethod
def crear_reservacion(id_pasajero: int,
                      id_vuelo: int,
                      precio: float):

    connection = get_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor()
        connection.start_transaction()

        # 1️⃣ Verificar disponibilidad
        capacidad_query = """
            SELECT v.capacidad - COUNT(r.id_reservacion)
            FROM vuelo v
            LEFT JOIN reservacion r ON v.id_vuelo = r.id_vuelo
            WHERE v.id_vuelo = %s
            GROUP BY v.capacidad
        """

        cursor.execute(capacidad_query, (id_vuelo,))
        result = cursor.fetchone()

        if not result or result[0] <= 0:
            connection.rollback()
            return None

        # 2️⃣ Insertar reservación
        cursor.execute("""
            INSERT INTO reservacion (
                id_pasajero,
                id_vuelo,
                precio_pagado
            )
            VALUES (%s, %s, %s)
        """, (id_pasajero, id_vuelo, precio))

        id_reservacion = cursor.lastrowid

        # 3️⃣ Calcular hora abordaje
        cursor.execute("SELECT fecha_hora FROM vuelo WHERE id_vuelo = %s",
                       (id_vuelo,))
        vuelo_fecha = cursor.fetchone()[0]

        from datetime import timedelta
        hora_abordaje = vuelo_fecha - timedelta(minutes=30)

        # 4️⃣ Insertar pase SIN QR
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
        print("Error:", e)
        return None

    finally:
        close_connection(connection)
