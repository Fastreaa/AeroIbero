# core/servicios.py

from dao.pasajeros_dao import PasajeroDAO
from dao.vuelos_dao import VueloDAO
from dao.reservacion_dao import ReservacionDAO
from dao.ruta_dao import RutaDAO


class ServiciosAeroIbero:
    # Registrar pasajero
    @staticmethod
    def registrar_pasajero(nombre,
                           fecha_nacimiento,
                           nacionalidad,
                           raza,
                           telefono,
                           correo):

        id_pasajero = PasajeroDAO.insert(
            nombre_completo=nombre,
            fecha_nacimiento=fecha_nacimiento,
            nacionalidad=nacionalidad,
            raza=raza,
            telefono=telefono,
            correo=correo
        )

        return id_pasajero

    # Buscar vuelos entre ciudades
    @staticmethod
    def buscar_vuelos(id_ciudad_origen,
                      id_ciudad_destino,
                      fecha):

        vuelos = VueloDAO.get_vuelos_por_ciudades(
            id_ciudad_origen,
            id_ciudad_destino,
            fecha
        )

        return vuelos

    # Comprar boleto
    @staticmethod
    def comprar_boleto(id_pasajero,
                       id_vuelo,
                       precio):

        id_reservacion = ReservacionDAO.crear_reservacion(
            id_pasajero=id_pasajero,
            id_vuelo=id_vuelo,
            precio=precio
        )

        if not id_reservacion:
            return None

        return id_reservacion

    # Obtener pase completo
    @staticmethod
    def obtener_pase(id_reservacion):

        detalle = ReservacionDAO.get_detalle_reservacion(
            id_reservacion
        )

        if not detalle:
            return None

        # Generar QR dinámicamente (no guardado en BD)
        #qr = f"{detalle['numero_cliente']}-{detalle['numero_vuelo']}-{id_reservacion}"

        #detalle["qr_generado"] = qr

        return detalle