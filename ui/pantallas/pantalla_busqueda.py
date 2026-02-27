import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Callable, Dict, List

from core.servicios import ServiciosAeroIbero
from dao.ciudad_dao import CiudadDAO


class PantallaBusqueda(ttk.Frame):
    def __init__(self, master, app_state: Dict, on_next: Callable[[], None]):
        super().__init__(master, padding=16)
        self.app_state = app_state
        self.on_next = on_next

        self.origen_var = tk.StringVar()
        self.destino_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.criterio_var = tk.StringVar(value="costo")

        self._build()
        self._cargar_ciudades()

    def _build(self):
        ttk.Label(self, text="1) Buscar vuelo", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))

        grid = ttk.Frame(self)
        grid.pack(fill="x")
        grid.columnconfigure(1, weight=1)

        ttk.Label(grid, text="Origen").grid(row=0, column=0, sticky="w", pady=6)
        self.origen_cb = ttk.Combobox(grid, textvariable=self.origen_var, state="readonly")
        self.origen_cb.grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(grid, text="Destino").grid(row=1, column=0, sticky="w", pady=6)
        self.destino_cb = ttk.Combobox(grid, textvariable=self.destino_var, state="readonly")
        self.destino_cb.grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Label(grid, text="Fecha (YYYY-MM-DD)").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(grid, textvariable=self.fecha_var).grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(grid, text="Criterio").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Combobox(
            grid,
            textvariable=self.criterio_var,
            values=["costo", "tiempo", "distancia"],
            state="readonly",
        ).grid(row=3, column=1, sticky="ew", pady=6)

        ttk.Button(self, text="Buscar y continuar", command=self._buscar).pack(anchor="e", pady=(14, 0))

    def _cargar_ciudades(self):
        try:
            ciudades = [c["nombre"] for c in CiudadDAO.get_all() if c.get("nombre")]
        except Exception:
            ciudades = []

        ciudades = sorted(set(ciudades))
        self.origen_cb["values"] = ciudades
        self.destino_cb["values"] = ciudades

        if len(ciudades) >= 2:
            self.origen_var.set(ciudades[0])
            self.destino_var.set(ciudades[1])

    def _crear_opciones(self, base: Dict) -> List[Dict]:
        # Puedes reemplazar esta estrategia por vuelos reales en BD.
        costo = float(base["costo_total"])
        criterio = base["criterio"]
        return [
            {
                "nombre": "Opción Económica",
                "criterio": criterio,
                "camino": base["camino"],
                "costo_total": round(costo, 2),
            },
            {
                "nombre": "Opción Flexible",
                "criterio": criterio,
                "camino": base["camino"],
                "costo_total": round(costo * 1.08, 2),
            },
            {
                "nombre": "Opción Premium",
                "criterio": criterio,
                "camino": base["camino"],
                "costo_total": round(costo * 1.16, 2),
            },
        ]

    def _buscar(self):
        origen = self.origen_var.get().strip()
        destino = self.destino_var.get().strip()
        fecha = self.fecha_var.get().strip()
        criterio = self.criterio_var.get().strip()

        if not origen or not destino:
            messagebox.showwarning("Campos requeridos", "Selecciona origen y destino")
            return

        if origen == destino:
            messagebox.showwarning("Ruta inválida", "Origen y destino deben ser distintos")
            return

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Fecha inválida", "La fecha debe tener formato YYYY-MM-DD")
            return

        try:
            resultado = ServiciosAeroIbero.ejecutar_dijkstra(origen, destino, criterio)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular ruta: {e}")
            return

        if not resultado.get("camino"):
            messagebox.showwarning("Sin ruta", "No existe ruta para esa búsqueda")
            return

        self.app_state["busqueda"] = {
            "origen": origen,
            "destino": destino,
            "fecha": fecha,
            "criterio": criterio,
        }
        self.app_state["opciones"] = self._crear_opciones(resultado)
        self.on_next()
