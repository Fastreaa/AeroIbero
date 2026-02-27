# database.py

try:
    import mysql.connector
    from mysql.connector import Error
except ModuleNotFoundError:  # entorno sin mysql-connector
    mysql = None
    Error = Exception

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "12345",
    "database": "aeroibero",
    "port": 3306,
}


def get_connection():
    if mysql is None:
        print("mysql-connector no está instalado; se continuará sin conexión a BD")
        return None

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Conexión exitosa a MySQL")
            return connection
    except Error as e:
        print(f"Error al conectar: {e}")

    return None


def close_connection(connection):
    if connection and hasattr(connection, "is_connected") and connection.is_connected():
        connection.close()
        print("Conexión cerrada")
