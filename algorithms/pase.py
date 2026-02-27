
# algorithms/pase.py

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, Optional

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def _safe_text(value: Optional[object]) -> str:
    return "" if value is None else str(value)


def _file_safe(value: str) -> str:
    return "".join(ch for ch in value if ch.isalnum() or ch in ("-", "_")) or "pase"


def generar_pase_abordar_pdf(datos: Dict[str, object], output_dir: str = "pases") -> str:
    """
    Genera un PDF de pase de abordar con QR usando el detalle de reservación.

    Campos esperados en `datos`:
    - id_reservacion, numero_vuelo, nombre_completo, numero_cliente
    - ciudad_origen, ciudad_destino, fecha_hora, hora_abordaje, sala, puerta
    - opcionales: total_dinero, total_tiempo, total_distancia
    """

    os.makedirs(output_dir, exist_ok=True)

    id_reservacion = _safe_text(datos.get("id_reservacion"))
    numero_vuelo = _safe_text(datos.get("numero_vuelo"))
    nombre_completo = _safe_text(datos.get("nombre_completo"))
    numero_cliente = _safe_text(datos.get("numero_cliente"))
    ciudad_origen = _safe_text(datos.get("ciudad_origen"))
    ciudad_destino = _safe_text(datos.get("ciudad_destino"))
    fecha_hora = _safe_text(datos.get("fecha_hora"))
    hora_abordaje = _safe_text(datos.get("hora_abordaje"))
    sala = _safe_text(datos.get("sala"))
    puerta = _safe_text(datos.get("puerta"))
    total_dinero = _safe_text(datos.get("total_dinero"))
    total_tiempo = _safe_text(datos.get("total_tiempo"))
    total_distancia = _safe_text(datos.get("total_distancia"))

    nombre_archivo = _file_safe(f"pase_res_{id_reservacion}_{numero_vuelo}") + ".pdf"
    pdf_path = os.path.join(output_dir, nombre_archivo)

    qr_payload = (
        f"RES:{id_reservacion}|VUELO:{numero_vuelo}|CLIENTE:{numero_cliente}|"
        f"ORIGEN:{ciudad_origen}|DESTINO:{ciudad_destino}|SALA:{sala}|PUERTA:{puerta}"
    )

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setTitle(f"Pase de Abordar {id_reservacion}")
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "AeroIbero - Pase de Abordar")

    c.setFont("Helvetica", 11)
    y = height - 90
    line_gap = 18

    contenido = [
        ("Reservación", id_reservacion),
        ("Nombre pasajero", nombre_completo),
        ("Número de cliente", numero_cliente),
        ("Número de vuelo", numero_vuelo),
        ("Origen", ciudad_origen),
        ("Destino", ciudad_destino),
        ("Salida", fecha_hora),
        ("Hora de abordaje", hora_abordaje),
        ("Sala", sala),
        ("Puerta", puerta),


    if total_dinero:
        contenido.append(("Costo total", f"${total_dinero}"))
    if total_tiempo:
        contenido.append(("Tiempo total", total_tiempo))
    if total_distancia:
        contenido.append(("Distancia total", total_distancia))


    contenido.append(("Generado", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    contenido.append(("Generado", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    for etiqueta, valor in contenido:
        c.drawString(50, y, f"{etiqueta}: {valor}")
        y -= line_gap

    qr = QrCodeWidget(qr_payload)

    bounds = qr.getBounds()
    size = 150
    width_qr = bounds[2] - bounds[0]
    height_qr = bounds[3] - bounds[1]
    drawing = Drawing(
        size,
        size,
        transform=[size / width_qr, 0, 0, size / height_qr, 0, 0]
    )
    drawing.add(qr)
    renderPDF.draw(drawing, c, width - 210, height - 300)

    c.setFont("Helvetica", 9)
    c.drawString(width - 210, height - 315, "QR de validación del pase")

    c.showPage()
    c.save()

    return pdf_path

