import re
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict
from datetime import datetime, date

from core.database import get_connection, close_connection
from dao.ciudad_dao import CiudadDAO


class PantallaDatosPasajero(ttk.Frame):

    TELEFONO_REGEX = re.compile(r"^\+?\d{8,15}$")

    def __init__(self, master, app_state: Dict, on_back: Callable[[], None]):
        super().__init__(master, padding=16)

        self.app_state = app_state
        self.on_back = on_back

        # Información personal
        self.nombre_var = tk.StringVar()
        self.segundo_nombre_var = tk.StringVar()
        self.apellidos_var = tk.StringVar()
        self.nacimiento_var = tk.StringVar()
        self.raza_var = tk.StringVar()
        self.pais_var = tk.StringVar()

        # Contacto
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

        content = ttk.Frame(self)
        content.pack(fill="both", expand=True)

        left = ttk.Frame(content)
        left.pack(fill="both", expand=True)

        # ---------- Información personal ----------
        info_card = ttk.LabelFrame(left, text="Información personal", padding=12)
        info_card.pack(fill="x", pady=(0, 10))
        info_card.columnconfigure(1, weight=1)

        ttk.Label(info_card, text="Nombre").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(info_card, textvariable=self.nombre_var).grid(
            row=0, column=1, sticky="ew", pady=6
        )

        ttk.Label(info_card, text="Segundo nombre").grid(
            row=1, column=0, sticky="w", pady=6
        )
        ttk.Entry(info_card, textvariable=self.segundo_nombre_var).grid(
            row=1, column=1, sticky="ew", pady=6
        )

        ttk.Label(info_card, text="Apellidos").grid(
            row=2, column=0, sticky="w", pady=6
        )
        ttk.Entry(info_card, textvariable=self.apellidos_var).grid(
            row=2, column=1, sticky="ew", pady=6
        )

        ttk.Label(info_card, text="Fecha de nacimiento (YYYY-MM-DD)").grid(
            row=3, column=0, sticky="w", pady=6
        )
        ttk.Entry(info_card, textvariable=self.nacimiento_var).grid(
            row=3, column=1, sticky="ew", pady=6
        )

        ttk.Label(info_card, text="Raza").grid(
            row=4, column=0, sticky="w", pady=6
        )
        self.raza_cb = ttk.Combobox(
            info_card, textvariable=self.raza_var, state="readonly"
        )
        self.raza_cb.grid(row=4, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="País de residencia").grid(
            row=5, column=0, sticky="w", pady=6
        )
        self.pais_cb = ttk.Combobox(
            info_card, textvariable=self.pais_var, state="readonly"
        )
        self.pais_cb.grid(row=5, column=1, sticky="ew", pady=6)

        # ---------- Contacto ----------
        contacto_card = ttk.LabelFrame(
            left, text="Información de contacto", padding=12
        )
        contacto_card.pack(fill="x", pady=(0, 10))
        contacto_card.columnconfigure(1, weight=1)

        ttk.Label(contacto_card, text="Teléfono").grid(
            row=0, column=0, sticky="w", pady=6
        )
        ttk.Entry(contacto_card, textvariable=self.telefono_var).grid(
            row=0, column=1, sticky="ew", pady=6
        )

        ttk.Label(contacto_card, text="Correo electrónico").grid(
            row=1, column=0, sticky="w", pady=6
        )
        ttk.Entry(contacto_card, textvariable=self.correo_var).grid(
            row=1, column=1, sticky="ew", pady=6
        )

        self.resumen_label = ttk.Label(left, justify="left")
        self.resumen_label.pack(anchor="w", fill="x", pady=(4, 10))

        # ---------- Botones ----------
        actions = ttk.Frame(left)
        actions.pack(fill="x")

        ttk.Button(actions, text="Atrás", command=self.on_back).pack(side="left")
        ttk.Button(
            actions,
            text="Generar pase de abordar",
            command=self._generar_pase,
        ).pack(side="right")

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
            return False, "La fecha no puede ser futura"

        telefono = self.telefono_var.get().strip()
        if not telefono:
            return False, "Teléfono es obligatorio"

        if not self.TELEFONO_REGEX.fullmatch(telefono):
            return False, "Teléfono inválido"

        correo = self.correo_var.get().strip()
        if "@" not in correo or "." not in correo:
            return False, "Correo inválido"

        return True, ""

    def _generar_pase(self):
        ok, msg = self._validar_datos()
        if not ok:
            messagebox.showwarning("Datos inválidos", msg)
            return

        messagebox.showinfo("Éxito", "Datos validados correctamente")
