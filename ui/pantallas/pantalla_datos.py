import re
import tkinter as tk

from tkinter import ttk, messagebox
from typing import Callable, Dict
from datetime import datetime, date

from core.database import get_connection, close_connection
from dao.ciudad_dao import CiudadDAO


from core.database import close_connection, get_connection

class PantallaDatosPasajero(ttk.Frame):

    TELEFONO_REGEX = re.compile(r"^\+?[\d\s\-()]{8,20}$")


    def __init__(self, master, app_state: Dict, on_back: Callable[[], None]):
        super().__init__(master, padding=16)

        self.app_state = app_state
        self.on_back = on_back

        self.nombre_var = tk.StringVar()
        self.segundo_nombre_var = tk.StringVar()
        self.apellidos_var = tk.StringVar()
        self.nacimiento_var = tk.StringVar()
        self.raza_var = tk.StringVar()
        self.pais_var = tk.StringVar()

        self.telefono_var = tk.StringVar()
        self.correo_var = tk.StringVar()

        self._build()
        self._cargar_catalogos()

    def _build(self):
        ttk.Label(
            self,
            text="3) Información de pasajeros",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        left = ttk.Frame(self)

        left.pack(fill="both", expand=True)

        # ---------- Información personal ----------
        info_card = ttk.LabelFrame(left, text="Información personal", padding=12)
        info_card.pack(fill="x", pady=(0, 10))
        info_card.columnconfigure(1, weight=1)

        ttk.Label(info_card, text="Nombre").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(info_card, textvariable=self.nombre_var).grid(
            row=0, column=1, sticky="ew", pady=6
        )


        ttk.Label(info_card, text="Fecha de nacimiento (YYYY-MM-DD)").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Entry(info_card, textvariable=self.nacimiento_var).grid(row=3, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="Raza").grid(row=4, column=0, sticky="w", pady=6)
        self.raza_cb = ttk.Combobox(info_card, textvariable=self.raza_var, state="readonly")
        self.raza_cb.grid(row=4, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="País de residencia").grid(row=5, column=0, sticky="w", pady=6)
        self.pais_cb = ttk.Combobox(info_card, textvariable=self.pais_var, state="readonly")

        self.pais_cb.grid(row=5, column=1, sticky="ew", pady=6)

        # ---------- Contacto ----------
        contacto_card = ttk.LabelFrame(
            left, text="Información de contacto", padding=12
        )
        contacto_card.pack(fill="x", pady=(0, 10))
        contacto_card.columnconfigure(1, weight=1)


        ttk.Label(contacto_card, text="Teléfono").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(contacto_card, textvariable=self.telefono_var).grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(contacto_card, text="Correo electrónico").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(contacto_card, textvariable=self.correo_var).grid(row=1, column=1, sticky="ew", pady=6)


        self.resumen_label = ttk.Label(left, justify="left")
        self.resumen_label.pack(anchor="w", fill="x", pady=(4, 10))

        # ---------- Botones ----------
        actions = ttk.Frame(left)
        actions.pack(fill="x")

        ttk.Button(actions, text="Atrás", command=self.on_back).pack(side="left")
        ttk.Button(actions, text="Generar pase de abordar", command=self._generar_pase).pack(side="right")


    def _cargar_catalogos(self):
        self.pais_cb["values"] = self._obtener_paises()
        if self.pais_cb["values"]:
            self.pais_var.set(self.pais_cb["values"][0])

        self.raza_cb["values"] = self._obtener_razas()
        if self.raza_cb["values"]:
            self.raza_var.set(self.raza_cb["values"][0])

    @staticmethod
    def _obtener_paises():
        connection = get_connection()
        if not connection:
            return ["México", "Colombia", "España", "Argentina"]

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT nombre FROM pais ORDER BY nombre")
            rows = cursor.fetchall()
            return [r[0] for r in rows if r and r[0]]
        except Exception:
            return ["México", "Colombia", "España", "Argentina"]
        finally:
            close_connection(connection)

    @staticmethod
    def _obtener_razas():
        connection = get_connection()
        if not connection:
            return ["Mestiza", "Afrodescendiente", "Indígena", "Caucásica", "Otra"]

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT nombre FROM raza ORDER BY nombre")
            rows = cursor.fetchall()
            return [r[0] for r in rows if r and r[0]]
        except Exception:
            return ["Mestiza", "Afrodescendiente", "Indígena", "Caucásica", "Otra"]
        finally:
            close_connection(connection)

    def _validar_datos(self):
        if not self.nombre_var.get().strip() or not self.apellidos_var.get().strip():
            return False, "Nombre y apellidos son obligatorios"

        nacimiento_raw = self.nacimiento_var.get().strip()
        if not nacimiento_raw:
            return False, "Fecha de nacimiento es obligatoria"

        try:
            nacimiento = datetime.strptime(nacimiento_raw, "%Y-%m-%d").date()
        except ValueError:
            return False, "Fecha inválida (usa YYYY-MM-DD)"

        if nacimiento > date.today():

            return False, "La fecha de nacimiento no puede ser posterior al día de hoy"

        telefono = self.telefono_var.get().strip()
        if not telefono:
            return False, "Teléfono es obligatorio"

        if not self.TELEFONO_REGEX.fullmatch(telefono):
            return False, "Teléfono inválido"

        solo_digitos = re.sub(r"\D", "", telefono)
        if len(solo_digitos) < 8 or len(solo_digitos) > 15:
            return False, "Teléfono inválido. Debe contener entre 8 y 15 dígitos"

        correo = self.correo_var.get().strip()
        if "@" not in correo or "." not in correo:
            return False, "Correo electrónico inválido"

        return True, ""

    @staticmethod
    def _total_criterio(origen: str, destino: str, criterio: str) -> Optional[float]:
        from core.servicios import ServiciosAeroIbero

        try:
            resultado = ServiciosAeroIbero.ejecutar_dijkstra(origen, destino, criterio)
            return float(resultado.get("costo_total", 0))
        except Exception:
            return None

    @staticmethod
    def _safe_float(value) -> Optional[float]:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _totales_pdf(self, busqueda: Dict, opcion: Dict) -> Dict[str, Optional[float]]:
        origen = busqueda.get("origen", "")
        destino = busqueda.get("destino", "")

        totales = {
            "costo": self._total_criterio(origen, destino, "costo"),
            "tiempo": self._total_criterio(origen, destino, "tiempo"),
            "distancia": self._total_criterio(origen, destino, "distancia"),
        }

        criterio_opcion = opcion.get("criterio")
        costo_opcion = self._safe_float(opcion.get("costo_total"))
        if criterio_opcion in totales and totales[criterio_opcion] is None and costo_opcion is not None:
            totales[criterio_opcion] = costo_opcion

        if totales["costo"] is None and costo_opcion is not None:
            totales["costo"] = costo_opcion

        return totales

    def _generar_pase(self):
        ok, msg = self._validar_datos()
        if not ok:
            messagebox.showwarning("Datos inválidos", msg)
            return


        busqueda = self.app_state.get("busqueda", {})
        opcion = self.app_state.get("opcion_elegida", {})

        if not busqueda or not opcion:
            messagebox.showwarning("Flujo incompleto", "Primero busca y elige una opción")
            return

        nombre_completo = (
            f"{self.nombre_var.get().strip()} {self.segundo_nombre_var.get().strip()} {self.apellidos_var.get().strip()}"
            .replace("  ", " ")
            .strip()
        )
        numero_vuelo = f"AI-{abs(hash('|'.join(opcion.get('camino', [])))) % 9000 + 1000}"

        try:
            totales = self._totales_pdf(busqueda, opcion)
        except Exception:
            totales = {"costo": None, "tiempo": None, "distancia": None}

        fecha_vuelo = busqueda.get("fecha") or date.today().isoformat()
        datos_pase = {
            "id_reservacion": abs(hash(self.correo_var.get().strip() + numero_vuelo)) % 100000,
            "numero_vuelo": numero_vuelo,
            "nombre_completo": nombre_completo,
            "numero_cliente": f"CL-{abs(hash(self.telefono_var.get().strip())) % 999999:06d}",
            "ciudad_origen": busqueda.get("origen"),
            "ciudad_destino": busqueda.get("destino"),
            "fecha_hora": f"{fecha_vuelo} 08:00:00",
            "hora_abordaje": f"{fecha_vuelo} 07:30:00",
            "sala": 1,
            "puerta": 2,
            "total_dinero": round(totales["costo"], 2) if totales["costo"] is not None else "N/D",
            "total_tiempo": round(totales["tiempo"], 2) if totales["tiempo"] is not None else "N/D",
            "total_distancia": round(totales["distancia"], 2) if totales["distancia"] is not None else "N/D",
        }

        try:
            from algorithms.pase import generar_pase_abordar_pdf

            ruta_pdf = generar_pase_abordar_pdf(datos_pase, output_dir="pases")
        except Exception as e:
            messagebox.showerror(
                "Error al generar pase",
                f"No se pudo generar el PDF. Detalle: {e}\n"
                "Si el error menciona reportlab, instala la dependencia con: pip install reportlab",
            )
            return

        self.resumen_label.config(
            text=(
                f"Ruta: {' -> '.join(opcion.get('camino', []))}\n"
                f"Fecha: {fecha_vuelo}\n"
                f"Costo total: {datos_pase['total_dinero']}\n"
                f"Tiempo total: {datos_pase['total_tiempo']}\n"
                f"Distancia total: {datos_pase['total_distancia']}\n"
                f"País: {self.pais_var.get()}\n"
                f"Raza: {self.raza_var.get()}\n"
                f"PDF: {ruta_pdf}"
            )
        )
        messagebox.showinfo("Pase generado", f"Pase generado correctamente en:\n{ruta_pdf}")

