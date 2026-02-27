import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict



class PantallaDatosPasajero(ttk.Frame):
    def __init__(self, master, app_state: Dict, on_back: Callable[[], None]):
        super().__init__(master, padding=16)
        self.app_state = app_state
        self.on_back = on_back

        self.nombre_var = tk.StringVar()
        self.cliente_var = tk.StringVar()
        self.correo_var = tk.StringVar()

        self._build()

    def _build(self):
        ttk.Label(self, text="3) Datos del pasajero y pase", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))

        grid = ttk.Frame(self)
        grid.pack(fill="x")
        grid.columnconfigure(1, weight=1)

        ttk.Label(grid, text="Nombre completo").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(grid, textvariable=self.nombre_var).grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(grid, text="Número cliente").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(grid, textvariable=self.cliente_var).grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Label(grid, text="Correo").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(grid, textvariable=self.correo_var).grid(row=2, column=1, sticky="ew", pady=6)

        self.resultado = tk.Text(self, height=8, wrap="word")
        self.resultado.pack(fill="both", expand=True, pady=(12, 0))

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(10, 0))
        ttk.Button(actions, text="Atrás", command=self.on_back).pack(side="left")
        ttk.Button(actions, text="Generar pase", command=self._generar_pase).pack(side="right")

    def _generar_pase(self):
        nombre = self.nombre_var.get().strip()
        cliente = self.cliente_var.get().strip()
        correo = self.correo_var.get().strip()

        if not nombre or not cliente or not correo:
            messagebox.showwarning("Campos requeridos", "Completa todos los datos del pasajero")
            return

        busqueda = self.app_state.get("busqueda", {})
        opcion = self.app_state.get("opcion_elegida", {})

        if not busqueda or not opcion:
            messagebox.showwarning("Flujo incompleto", "Primero busca y elige una opción")
            return

        numero_vuelo = f"AI-{abs(hash('|'.join(opcion.get('camino', [])))) % 9000 + 1000}"
        datos_pase = {
            "id_reservacion": abs(hash(cliente + numero_vuelo)) % 100000,
            "numero_vuelo": numero_vuelo,
            "nombre_completo": nombre,
            "numero_cliente": cliente,
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

        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(
            tk.END,
            f"Pase generado correctamente.\n"
            f"Pasajero: {nombre}\n"
            f"Ruta: {' -> '.join(opcion.get('camino', []))}\n"
            f"Total: ${opcion.get('costo_total')}\n"
            f"Archivo: {ruta_pdf}\n"
        )
