
# ui/interfaz.py

from __future__ import annotations

import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from core.servicios import ServiciosAeroIbero
from dao.ciudad_dao import CiudadDAO
from core.database import get_connection, close_connection
from algorithms.pase import generar_pase_abordar_pdf


class AeroIberoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AeroIbero")
        self.geometry("1080x680")
        self.minsize(980, 620)

        self.pasajeros = tk.IntVar(value=1)
        self.route_mode = tk.StringVar(value="ida")
        self.criterio = tk.StringVar(value="costo")
        self.origen_var = tk.StringVar()
        self.destino_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.opciones_generadas: list[dict] = []
        self.opcion_seleccionada = tk.IntVar(value=-1)
        self.opcion_elegida: dict | None = None
        self.totales_ruta = {"costo": 0.0, "tiempo": 0.0, "distancia": 0.0}

        self._build_ui()
        self._cargar_ciudades()

    def _build_ui(self):
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)

        title = ttk.Label(
            root,
            text="¡Bienvenidx a AeroIbero!",
            font=("Segoe UI", 28, "bold"),
        )
        title.pack(anchor="w", pady=(0, 18))

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        self.tab_reserva = ttk.Frame(self.tabs, padding=14)
        self.tab_opciones = ttk.Frame(self.tabs, padding=14)
        self.tab_datos = ttk.Frame(self.tabs, padding=14)
        self.tab_estado = ttk.Frame(self.tabs, padding=14)
        self.tabs.add(self.tab_reserva, text="Mi Reserva")
        self.tabs.add(self.tab_opciones, text="2) Opciones")
        self.tabs.add(self.tab_datos, text="3) Datos y Pase")
        self.tabs.add(self.tab_estado, text="Estados")

        self._build_tab_reserva()
        self._build_tab_opciones()
        self._build_tab_datos()
        self._build_tab_estado()

    def _build_tab_reserva(self):
        container = ttk.Frame(self.tab_reserva)
        container.pack(fill="both", expand=True)

        left = ttk.Frame(container)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        right = ttk.LabelFrame(container, text="Resumen")
        right.pack(side="right", fill="y")

        ttk.Label(left, text="Busca tu vuelo", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))

        mode_row = ttk.Frame(left)
        mode_row.pack(fill="x", pady=(0, 10))
        ttk.Radiobutton(mode_row, text="Ida", variable=self.route_mode, value="ida").pack(side="left", padx=(0, 12))
        ttk.Radiobutton(mode_row, text="Multidestino", variable=self.route_mode, value="multidestino").pack(side="left")

        grid = ttk.Frame(left)
        grid.pack(fill="x")
        grid.columnconfigure(1, weight=1)

        ttk.Label(grid, text="Ciudad de origen").grid(row=0, column=0, sticky="w", pady=6)
        self.origen_cb = ttk.Combobox(grid, textvariable=self.origen_var, state="readonly")
        self.origen_cb.grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(grid, text="Destino").grid(row=1, column=0, sticky="w", pady=6)
        self.destino_cb = ttk.Combobox(grid, textvariable=self.destino_var, state="readonly")
        self.destino_cb.grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Label(grid, text="Fecha (YYYY-MM-DD)").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(grid, textvariable=self.fecha_var).grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(grid, text="Criterio").grid(row=3, column=0, sticky="w", pady=6)
        criterio_cb = ttk.Combobox(
            grid,
            textvariable=self.criterio,
            state="readonly",
            values=["costo", "tiempo", "distancia"],
        )
        criterio_cb.grid(row=3, column=1, sticky="ew", pady=6)

        pax_row = ttk.Frame(left)
        pax_row.pack(anchor="w", pady=(10, 8))
        ttk.Label(pax_row, text="Pasajeros", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 8))
        ttk.Button(pax_row, text="-", width=3, command=self._decrementar_pasajeros).pack(side="left")
        ttk.Label(pax_row, textvariable=self.pasajeros, width=4, anchor="center").pack(side="left")
        ttk.Button(pax_row, text="+", width=3, command=self._incrementar_pasajeros).pack(side="left")

        actions = ttk.Frame(left)
        actions.pack(anchor="w", pady=(6, 14))
        ttk.Button(actions, text="Intercambiar", command=self._intercambiar_ciudades).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Limpiar", command=self._limpiar_busqueda).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Buscar Vuelo", command=self._buscar_vuelo).pack(side="left", padx=(0, 8))
        self.btn_ir_opciones = ttk.Button(actions, text="Ir a opciones", command=self._ir_a_opciones, state="disabled")
        self.btn_ir_opciones.pack(side="left")

        self.resultado = tk.Text(left, height=10, wrap="word")
        self.resultado.pack(fill="both", expand=True)

        self.resumen_label = ttk.Label(
            right,
            text=(
                "Aquí verás:\n"
                "• Ruta sugerida\n"
                "• Costo/tiempo/distancia\n"
                "• Pasajeros seleccionados"
            ),
            justify="left",
            padding=12,
        )
        self.resumen_label.pack(anchor="nw")

    def _build_tab_opciones(self):
        ttk.Label(self.tab_opciones, text="2) Selecciona tu opción", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

        self.opciones_info = ttk.Label(
            self.tab_opciones,
            text="Primero realiza una búsqueda en la pestaña 'Mi Reserva'.",
            justify="left",
        )
        self.opciones_info.pack(anchor="w", pady=(0, 8))

        self.opciones_container = ttk.Frame(self.tab_opciones)
        self.opciones_container.pack(fill="both", expand=True)

        actions = ttk.Frame(self.tab_opciones)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Volver a búsqueda", command=lambda: self.tabs.select(self.tab_reserva)).pack(side="left")
        ttk.Button(actions, text="Seleccionar opción", command=self._seleccionar_opcion).pack(side="right")

    def _build_tab_datos(self):
        ttk.Label(self.tab_datos, text="3) Captura tus datos y genera pase", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

        form = ttk.Frame(self.tab_datos)
        form.pack(fill="x", pady=(0, 10))
        form.columnconfigure(1, weight=1)

        self.nombre_var = tk.StringVar()
        self.cliente_var = tk.StringVar()
        self.correo_var = tk.StringVar()

        ttk.Label(form, text="Nombre completo").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.nombre_var).grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(form, text="Número cliente").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.cliente_var).grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(form, text="Correo").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.correo_var).grid(row=2, column=1, sticky="ew", pady=4)

        self.resumen_datos = ttk.Label(
            self.tab_datos,
            text="Selecciona una opción en la pestaña 2 para ver totales y generar pase.",
            justify="left",
        )
        self.resumen_datos.pack(anchor="w", pady=(0, 8))

        actions = ttk.Frame(self.tab_datos)
        actions.pack(fill="x")
        ttk.Button(actions, text="Volver a opciones", command=lambda: self.tabs.select(self.tab_opciones)).pack(side="left")
        ttk.Button(actions, text="Generar pase de abordar", command=self._generar_pase_desde_datos).pack(side="right")

    def _build_tab_estado(self):
        ttk.Label(self.tab_estado, text="Consulta estado de reservación", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 12))

        row = ttk.Frame(self.tab_estado)
        row.pack(fill="x")

        ttk.Label(row, text="ID Reservación").pack(side="left")
        self.id_res_var = tk.StringVar()
        ttk.Entry(row, textvariable=self.id_res_var, width=20).pack(side="left", padx=8)
        ttk.Button(row, text="Consultar", command=self._consultar_estado).pack(side="left")

        self.estado_text = tk.Text(self.tab_estado, height=16, wrap="word")
        self.estado_text.pack(fill="both", expand=True, pady=(12, 0))

    def _cargar_ciudades(self):
        ciudades = []
        try:
            ciudades_db = CiudadDAO.get_all()
            ciudades = [c["nombre"] for c in ciudades_db if c.get("nombre")]
        except Exception:
            ciudades = []

        if not ciudades:
            ciudades = self._ciudades_desde_csv()

        ciudades = sorted(set(ciudades))
        self.origen_cb["values"] = ciudades
        self.destino_cb["values"] = ciudades

        if ciudades:
            self.origen_var.set(ciudades[0])
            if len(ciudades) > 1:
                self.destino_var.set(ciudades[1])

    @staticmethod
    def _ciudades_desde_csv() -> list[str]:
        ciudades = set()
        try:
            with open("Ciudades_Aeroibero.csv", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ciudades.add(row.get("Origen", "").strip())
                    ciudades.add(row.get("Destino", "").strip())
        except Exception:
            return []
        return [c for c in ciudades if c]

    def _incrementar_pasajeros(self):
        if self.pasajeros.get() < 20:
            self.pasajeros.set(self.pasajeros.get() + 1)

    def _decrementar_pasajeros(self):
        if self.pasajeros.get() > 1:
            self.pasajeros.set(self.pasajeros.get() - 1)

    def _intercambiar_ciudades(self):
        origen = self.origen_var.get()
        destino = self.destino_var.get()
        self.origen_var.set(destino)
        self.destino_var.set(origen)

    def _limpiar_busqueda(self):
        self.fecha_var.set("")
        self.criterio.set("costo")
        self.route_mode.set("ida")
        self.pasajeros.set(1)
        self.resultado.delete("1.0", tk.END)
        self.resumen_label.config(text="Aquí verás:\n• Ruta sugerida\n• Costo/tiempo/distancia\n• Pasajeros seleccionados")
        self.opciones_generadas = []
        self.opcion_seleccionada.set(-1)
        self.opcion_elegida = None
        self.btn_ir_opciones.configure(state="disabled")
        self._render_opciones()
        if hasattr(self, "resumen_datos"):
            self.resumen_datos.config(text="Selecciona una opción en la pestaña 2 para ver totales y generar pase.")

    def _buscar_vuelo(self):
        origen = self.origen_var.get().strip()
        destino = self.destino_var.get().strip()
        fecha = self.fecha_var.get().strip()
        criterio = self.criterio.get().strip()

        if not origen or not destino:
            messagebox.showwarning("Campos requeridos", "Debes seleccionar origen y destino.")
            return

        if origen == destino:
            messagebox.showwarning("Ruta inválida", "Origen y destino deben ser diferentes.")
            return

        if fecha:
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Fecha inválida", "La fecha debe tener formato YYYY-MM-DD.")
                return

        try:
            resultado = ServiciosAeroIbero.ejecutar_dijkstra(origen, destino, criterio)
        except Exception as e:
            messagebox.showerror("Error al buscar ruta", str(e))
            return

        self.resultado.delete("1.0", tk.END)

        if not resultado.get("camino"):
            self.resultado.insert(tk.END, "No se encontró una ruta disponible.\n")
            if resultado.get("mensaje"):
                self.resultado.insert(tk.END, resultado["mensaje"] + "\n")
            return

        camino = " -> ".join(resultado["camino"])
        costo = resultado["costo_total"]

        self.resultado.insert(tk.END, f"Modo: {self.route_mode.get()}\n")
        self.resultado.insert(tk.END, f"Fecha: {fecha or 'No especificada'}\n")
        self.resultado.insert(tk.END, f"Criterio: {criterio}\n")
        self.resultado.insert(tk.END, f"Pasajeros: {self.pasajeros.get()}\n\n")
        self.resultado.insert(tk.END, f"Ruta óptima:\n{camino}\n")
        self.resultado.insert(tk.END, f"Costo total ({criterio}): {costo:.2f}\n")

        self.resumen_label.config(
            text=(
                f"Ruta: {camino}\n"
                f"Criterio: {criterio}\n"
                f"Costo total: {costo:.2f}\n"
                f"Pasajeros: {self.pasajeros.get()}"
            )
        )

        self.totales_ruta = self._calcular_totales(origen, destino)
        self.opciones_generadas = self._crear_opciones(resultado)
        self.opcion_seleccionada.set(0)
        self.opcion_elegida = None
        self.btn_ir_opciones.configure(state="normal")
        self._render_opciones()

    def _calcular_totales(self, origen: str, destino: str) -> dict:
        totales = {"costo": 0.0, "tiempo": 0.0, "distancia": 0.0}
        for criterio in ("costo", "tiempo", "distancia"):
            try:
                res = ServiciosAeroIbero.ejecutar_dijkstra(origen, destino, criterio)
                if res.get("camino"):
                    totales[criterio] = float(res.get("costo_total", 0.0))
            except Exception:
                pass
        return totales

    @staticmethod
    def _crear_opciones(resultado: dict) -> list[dict]:
        costo = float(resultado.get("costo_total", 0))
        criterio = resultado.get("criterio", "costo")
        camino = resultado.get("camino", [])
        return [
            {"nombre": "Opción Económica", "criterio": criterio, "camino": camino, "costo_total": round(costo, 2)},
            {"nombre": "Opción Flexible", "criterio": criterio, "camino": camino, "costo_total": round(costo * 1.08, 2)},
            {"nombre": "Opción Premium", "criterio": criterio, "camino": camino, "costo_total": round(costo * 1.16, 2)},
        ]

    def _render_opciones(self):
        for child in self.opciones_container.winfo_children():
            child.destroy()

        if not self.opciones_generadas:
            self.opciones_info.config(text="No hay opciones disponibles. Realiza una búsqueda primero.")
            return

        self.opciones_info.config(text="Elige una opción y presiona 'Seleccionar opción'.")

        for idx, op in enumerate(self.opciones_generadas):
            card = ttk.LabelFrame(self.opciones_container, text=op["nombre"], padding=10)
            card.pack(fill="x", pady=6)
            ttk.Label(card, text=f"Ruta: {' -> '.join(op.get('camino', []))}").pack(anchor="w")
            ttk.Label(card, text=f"Criterio: {op.get('criterio')}").pack(anchor="w")
            ttk.Label(card, text=f"Total: {op.get('costo_total', 0):.2f}", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Radiobutton(
                card,
                text="Seleccionar esta opción",
                variable=self.opcion_seleccionada,
                value=idx,
            ).pack(anchor="e", pady=(6, 0))

    def _ir_a_opciones(self):
        if not self.opciones_generadas:
            messagebox.showwarning("Sin opciones", "Primero realiza una búsqueda de vuelo.")
            return
        self.tabs.select(self.tab_opciones)

    def _seleccionar_opcion(self):
        idx = self.opcion_seleccionada.get()
        if idx < 0 or idx >= len(self.opciones_generadas):
            messagebox.showwarning("Selección requerida", "Selecciona una opción para continuar.")
            return

        opcion = self.opciones_generadas[idx]
        self.opcion_elegida = opcion

        self.resumen_label.config(
            text=(
                f"Ruta: {' -> '.join(opcion.get('camino', []))}\n"
                f"Criterio principal: {opcion.get('criterio')}\n"
                f"Costo opción: {opcion.get('costo_total', 0):.2f}\n"
                f"Totales ruta -> Costo:{self.totales_ruta.get('costo', 0):.2f} | "
                f"Tiempo:{self.totales_ruta.get('tiempo', 0):.2f} | "
                f"Distancia:{self.totales_ruta.get('distancia', 0):.2f}"
            )
        )

        self.resumen_datos.config(
            text=(
                f"Opción elegida: {opcion.get('nombre')}\n"
                f"Ruta: {' -> '.join(opcion.get('camino', []))}\n"
                f"Costo total: {self.totales_ruta.get('costo', 0):.2f}\n"
                f"Tiempo total: {self.totales_ruta.get('tiempo', 0):.2f}\n"
                f"Distancia total: {self.totales_ruta.get('distancia', 0):.2f}"
            )
        )

        messagebox.showinfo("Opción seleccionada", f"Seleccionaste: {opcion.get('nombre')}")
        self.tabs.select(self.tab_datos)

    def _generar_pase_desde_datos(self):
        if not self.opcion_elegida:
            messagebox.showwarning("Falta selección", "Primero selecciona una opción en la pestaña 2.")
            return

        nombre = self.nombre_var.get().strip()
        cliente = self.cliente_var.get().strip()
        correo = self.correo_var.get().strip()
        if not nombre or not cliente or not correo:
            messagebox.showwarning("Datos incompletos", "Completa nombre, número de cliente y correo.")
            return

        camino = self.opcion_elegida.get("camino", [])
        origen = camino[0] if camino else self.origen_var.get().strip()
        destino = camino[-1] if camino else self.destino_var.get().strip()

        datos_pase = {
            "id_reservacion": f"TMP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "numero_vuelo": "SIM-001",
            "nombre_completo": nombre,
            "numero_cliente": cliente,
            "correo": correo,
            "ciudad_origen": origen,
            "ciudad_destino": destino,
            "fecha_hora": self.fecha_var.get().strip() or datetime.now().strftime("%Y-%m-%d"),
            "hora_abordaje": "N/D",
            "sala": "Por asignar",
            "puerta": "Por asignar",
            "costo_total": f"{self.totales_ruta.get('costo', 0):.2f}",
            "tiempo_total": f"{self.totales_ruta.get('tiempo', 0):.2f}",
            "distancia_total": f"{self.totales_ruta.get('distancia', 0):.2f}",
        }

        try:
            pdf_path = generar_pase_abordar_pdf(datos_pase)
        except Exception as e:
            messagebox.showerror("Error al generar pase", str(e))
            return

        messagebox.showinfo("Pase generado", f"Pase de abordar generado en:\n{pdf_path}")

    def _consultar_estado(self):
        id_res = self.id_res_var.get().strip()
        if not id_res.isdigit():
            messagebox.showwarning("ID inválido", "Ingresa un ID de reservación numérico.")
            return

        connection = get_connection()
        if not connection:
            messagebox.showerror("Base de datos", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT
                    r.id_reservacion,
                    p.nombre_completo,
                    v.numero_vuelo,
                    v.fecha_hora,
                    pa.hora_abordaje,
                    v.sala,
                    v.puerta
                FROM reservacion r
                JOIN pasajero p ON p.id_pasajero = r.id_pasajero
                JOIN vuelo v ON v.id_vuelo = r.id_vuelo
                LEFT JOIN pase_abordar pa ON pa.id_reservacion = r.id_reservacion
                WHERE r.id_reservacion = %s
            """
            cursor.execute(query, (int(id_res),))
            data = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        finally:
            close_connection(connection)

        self.estado_text.delete("1.0", tk.END)

        if not data:
            self.estado_text.insert(tk.END, "No se encontró la reservación solicitada.\n")
            return

        self.estado_text.insert(tk.END, f"Reservación: {data['id_reservacion']}\n")
        self.estado_text.insert(tk.END, f"Pasajero: {data['nombre_completo']}\n")
        self.estado_text.insert(tk.END, f"Vuelo: {data['numero_vuelo']}\n")
        self.estado_text.insert(tk.END, f"Salida: {data['fecha_hora']}\n")
        self.estado_text.insert(tk.END, f"Hora de abordaje: {data.get('hora_abordaje')}\n")
        self.estado_text.insert(tk.END, f"Sala/Puerta: {data['sala']}/{data['puerta']}\n")


def run_app():
    app = AeroIberoApp()
    app.mainloop()


