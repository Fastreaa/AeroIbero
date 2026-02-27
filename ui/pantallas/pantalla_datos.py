import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict

from core.database import get_connection, close_connection
from dao.ciudad_dao import CiudadDAO


class PantallaDatosPasajero(ttk.Frame):
    def __init__(self, master, app_state: Dict, on_back: Callable[[], None]):
        super().__init__(master, padding=16)
        self.app_state = app_state
        self.on_back = on_back

        # Información personal
        self.nombre_var = tk.StringVar()
        self.segundo_nombre_var = tk.StringVar()
        self.apellidos_var = tk.StringVar()
        self.genero_var = tk.StringVar()
        self.nacimiento_var = tk.StringVar()
        self.raza_var = tk.StringVar()
        self.pais_var = tk.StringVar()
        self.ciudad_var = tk.StringVar()

        # Contacto
        self.telefono_var = tk.StringVar()
        self.correo_var = tk.StringVar()

        # Preferencias
        self.programa_frecuente_var = tk.StringVar()
        self.preferencia_alimento_var = tk.StringVar()
        self.silla_ruedas_var = tk.BooleanVar(value=False)
        self.newsletter_var = tk.BooleanVar(value=False)

        self._build()
        self._cargar_catalogos()

    def _build(self):
        ttk.Label(self, text="3) Información de pasajeros", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 10))

        content = ttk.Frame(self)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)

        # ---------------- IZQUIERDA: FORMULARIO ----------------
        left = ttk.Frame(content)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        info_card = ttk.LabelFrame(left, text="Información personal", padding=12)
        info_card.pack(fill="x", pady=(0, 10))
        info_card.columnconfigure(1, weight=1)

        ttk.Label(info_card, text="Nombre").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(info_card, textvariable=self.nombre_var).grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="Segundo nombre (opcional)").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(info_card, textvariable=self.segundo_nombre_var).grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="Apellidos").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(info_card, textvariable=self.apellidos_var).grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="Género").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Combobox(info_card, textvariable=self.genero_var, state="readonly", values=["Femenino", "Masculino", "Otro"]).grid(row=3, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="Fecha de nacimiento (YYYY-MM-DD)").grid(row=4, column=0, sticky="w", pady=6)
        ttk.Entry(info_card, textvariable=self.nacimiento_var).grid(row=4, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="Raza").grid(row=5, column=0, sticky="w", pady=6)
        self.raza_cb = ttk.Combobox(info_card, textvariable=self.raza_var, state="readonly")
        self.raza_cb.grid(row=5, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="País de residencia").grid(row=6, column=0, sticky="w", pady=6)
        self.pais_cb = ttk.Combobox(info_card, textvariable=self.pais_var, state="readonly")
        self.pais_cb.grid(row=6, column=1, sticky="ew", pady=6)

        ttk.Label(info_card, text="Ciudad").grid(row=7, column=0, sticky="w", pady=6)
        self.ciudad_cb = ttk.Combobox(info_card, textvariable=self.ciudad_var, state="readonly")
        self.ciudad_cb.grid(row=7, column=1, sticky="ew", pady=6)

        contacto_card = ttk.LabelFrame(left, text="Información de contacto", padding=12)
        contacto_card.pack(fill="x", pady=(0, 10))
        contacto_card.columnconfigure(1, weight=1)

        ttk.Label(contacto_card, text="Teléfono").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(contacto_card, textvariable=self.telefono_var).grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(contacto_card, text="Correo electrónico").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(contacto_card, textvariable=self.correo_var).grid(row=1, column=1, sticky="ew", pady=6)

        extra_card = ttk.LabelFrame(left, text="Detalles adicionales", padding=12)
        extra_card.pack(fill="x", pady=(0, 10))
        extra_card.columnconfigure(1, weight=1)

        ttk.Label(extra_card, text="Programa de viajero frecuente").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Combobox(
            extra_card,
            textvariable=self.programa_frecuente_var,
            state="readonly",
            values=["Ninguno", "AeroIbero Rewards", "SkyTeam", "Otro"],
        ).grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(extra_card, text="Preferencia de alimentos").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(
            extra_card,
            textvariable=self.preferencia_alimento_var,
            state="readonly",
            values=["Sin preferencia", "Vegetariano", "Vegano", "Sin gluten"],
        ).grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Checkbutton(extra_card, text="Requiero asistencia en silla de ruedas", variable=self.silla_ruedas_var).grid(row=2, column=0, columnspan=2, sticky="w", pady=4)
        ttk.Checkbutton(extra_card, text="Deseo recibir ofertas y promociones", variable=self.newsletter_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=4)

        actions = ttk.Frame(left)
        actions.pack(fill="x")
        ttk.Button(actions, text="Atrás", command=self.on_back).pack(side="left")
        ttk.Button(actions, text="Generar pase de abordar", command=self._generar_pase).pack(side="right")

        # ---------------- DERECHA: RESUMEN ----------------
        right = ttk.LabelFrame(content, text="Resumen de compra", padding=12)
        right.grid(row=0, column=1, sticky="nsew")

        self.resumen_label = ttk.Label(right, justify="left")
        self.resumen_label.pack(anchor="nw", fill="x")

        self.resultado = tk.Text(right, height=14, wrap="word")
        self.resultado.pack(fill="both", expand=True, pady=(10, 0))

    def _cargar_catalogos(self):
        # Ciudades
        try:
            ciudades = [c["nombre"] for c in CiudadDAO.get_all() if c.get("nombre")]
        except Exception:
            ciudades = []
        ciudades = sorted(set(ciudades))
        self.ciudad_cb["values"] = ciudades
        if ciudades:
            self.ciudad_var.set(ciudades[0])

        # Países
        self.pais_cb["values"] = self._obtener_paises()
        if self.pais_cb["values"]:
            self.pais_var.set(self.pais_cb["values"][0])

        # Razas
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
            values = [r[0] for r in rows if r and r[0]]
            return values or ["México", "Colombia", "España", "Argentina"]
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
            values = [r[0] for r in rows if r and r[0]]
            return values or ["Mestiza", "Afrodescendiente", "Indígena", "Caucásica", "Otra"]
        except Exception:
            return ["Mestiza", "Afrodescendiente", "Indígena", "Caucásica", "Otra"]
        finally:
            close_connection(connection)

    def _validar_datos(self):
        if not self.nombre_var.get().strip() or not self.apellidos_var.get().strip():
            return False, "Nombre y apellidos son obligatorios"

        if not self.nacimiento_var.get().strip():
            return False, "Fecha de nacimiento es obligatoria"

        try:
            from datetime import datetime
            datetime.strptime(self.nacimiento_var.get().strip(), "%Y-%m-%d")
        except ValueError:
            return False, "Fecha de nacimiento inválida (usa YYYY-MM-DD)"

        correo = self.correo_var.get().strip()
        if "@" not in correo or "." not in correo:
            return False, "Correo electrónico inválido"

        if not self.telefono_var.get().strip():
            return False, "Teléfono es obligatorio"

        return True, ""

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

        nombre_completo = f"{self.nombre_var.get().strip()} {self.segundo_nombre_var.get().strip()} {self.apellidos_var.get().strip()}".replace("  ", " ").strip()
        numero_vuelo = f"AI-{abs(hash('|'.join(opcion.get('camino', [])))) % 9000 + 1000}"

        datos_pase = {
            "id_reservacion": abs(hash(self.correo_var.get().strip() + numero_vuelo)) % 100000,
            "numero_vuelo": numero_vuelo,
            "nombre_completo": nombre_completo,
            "numero_cliente": f"CL-{abs(hash(self.telefono_var.get().strip())) % 999999:06d}",
            "ciudad_origen": busqueda.get("origen"),
            "ciudad_destino": busqueda.get("destino"),
            "fecha_hora": f"{busqueda.get('fecha')} 08:00:00",
            "hora_abordaje": f"{busqueda.get('fecha')} 07:30:00",
            "sala": 1,
            "puerta": 2,
        }

        try:
            from algorithms.pase import generar_pase_abordar_pdf
            ruta_pdf = generar_pase_abordar_pdf(datos_pase, output_dir="pases")
        except Exception as e:
            messagebox.showerror("Error al generar pase", str(e))
            return

        self.resumen_label.config(
            text=(
                f"Ruta: {' -> '.join(opcion.get('camino', []))}\n"
                f"Fecha: {busqueda.get('fecha')}\n"
                f"Criterio: {opcion.get('criterio')}\n"
                f"Total: ${opcion.get('costo_total')}\n"
                f"País: {self.pais_var.get()}\n"
                f"Ciudad: {self.ciudad_var.get()}\n"
                f"Raza: {self.raza_var.get()}"
            )
        )

        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(
            tk.END,
            f"Pase generado correctamente.\n"
            f"Pasajero: {nombre_completo}\n"
            f"Vuelo: {numero_vuelo}\n"
            f"Archivo: {ruta_pdf}\n"
            f"\nContacto\n"
            f"Teléfono: {self.telefono_var.get().strip()}\n"
            f"Correo: {self.correo_var.get().strip()}\n"
        )
