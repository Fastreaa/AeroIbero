import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict


class PantallaOpciones(ttk.Frame):
    def __init__(self, master, app_state: Dict, on_back: Callable[[], None], on_next: Callable[[], None]):
        super().__init__(master, padding=16)
        self.app_state = app_state
        self.on_back = on_back
        self.on_next = on_next
        self.index_var = tk.IntVar(value=-1)

        self._build()

    def _build(self):
        # Encabezado estilo buscador de aerolínea
        self.header_title = ttk.Label(
            self,
            text="Elige tu vuelo de salida",
            font=("Segoe UI", 22, "bold"),
        )
        self.header_title.pack(anchor="w")

        self.header_sub = ttk.Label(
            self,
            text="",
            font=("Segoe UI", 12),
            foreground="#3d4f66",
        )
        self.header_sub.pack(anchor="w", pady=(4, 14))

        # Barra de filtros/sort
        tools = ttk.Frame(self)
        tools.pack(fill="x", pady=(0, 10))

        ttk.Label(tools, text="Filtrar", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Label(tools, text="   Ordenar por").pack(side="left")

        self.sort_var = tk.StringVar(value="Recomendados")
        ttk.Combobox(
            tools,
            textvariable=self.sort_var,
            state="readonly",
            values=["Recomendados", "Menor precio", "Menor tiempo"],
            width=18,
        ).pack(side="left", padx=(6, 0))

        ttk.Button(tools, text="Aplicar", command=self.refrescar).pack(side="left", padx=(8, 0))

        # Contenedor de tarjetas de opciones
        self.cards_container = ttk.Frame(self)
        self.cards_container.pack(fill="both", expand=True)

        # Acciones
        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Atrás", command=self.on_back).pack(side="left")
        ttk.Button(actions, text="Continuar", command=self._continuar).pack(side="right")

    def _ordenar_opciones(self, opciones):
        criterio = self.sort_var.get()

        if criterio == "Menor precio":
            return sorted(opciones, key=lambda x: float(x.get("costo_total", 0)))

        if criterio == "Menor tiempo":
            # Simulación: menos escalas (longitud de camino) primero
            return sorted(opciones, key=lambda x: len(x.get("camino", [])))

        return opciones

    def _hora_demo(self, idx: int, llegada: bool = False) -> str:
        base_hora = 7 + idx
        minuto = 5 if idx % 2 == 0 else 35
        if llegada:
            base_hora += 4 + idx
            minuto = 45 if idx % 2 == 0 else 20
        return f"{base_hora:02d}:{minuto:02d}"

    def refrescar(self):
        for w in self.cards_container.winfo_children():
            w.destroy()

        busqueda = self.app_state.get("busqueda", {})
        origen = busqueda.get("origen", "---")
        destino = busqueda.get("destino", "---")
        fecha = busqueda.get("fecha", "---")
        self.header_sub.config(text=f"{origen} → {destino}  |  {fecha}")

        opciones = self.app_state.get("opciones", [])
        opciones = self._ordenar_opciones(opciones)
        self.index_var.set(0 if opciones else -1)

        if not opciones:
            ttk.Label(
                self.cards_container,
                text="No hay opciones disponibles. Regresa a la búsqueda.",
                foreground="#8a1c1c",
                font=("Segoe UI", 11, "bold"),
            ).pack(anchor="w", pady=10)
            return

        for i, op in enumerate(opciones):
            card = ttk.LabelFrame(self.cards_container, text=f"Opción {i+1}: {op['nombre']}", padding=10)
            card.pack(fill="x", pady=6)

            # Fila principal estilo itinerario + tarifas
            row = ttk.Frame(card)
            row.pack(fill="x")

            # bloque de ruta/hora
            left = ttk.Frame(row)
            left.pack(side="left", fill="x", expand=True)

            salida = self._hora_demo(i, llegada=False)
            llegada = self._hora_demo(i, llegada=True)
            ruta = " → ".join(op.get("camino", []))
            escalas = max(len(op.get("camino", [])) - 2, 0)

            ttk.Label(left, text=f"{salida}   ───────────   {llegada}", font=("Segoe UI", 14, "bold")).pack(anchor="w")
            ttk.Label(left, text=ruta, foreground="#1b2b4a").pack(anchor="w", pady=(2, 0))
            ttk.Label(left, text=f"{escalas} escala(s) | criterio: {op.get('criterio')}", foreground="#44546a").pack(anchor="w")

            # bloque tarifas estilo columnas
            fare = ttk.Frame(row)
            fare.pack(side="right")

            total = float(op.get("costo_total", 0))
            tarifas = [
                ("Main", total),
                ("AM+", round(total * 1.18, 2)),
                ("Premier", round(total * 1.36, 2)),
            ]

            for nombre, precio in tarifas:
                col = ttk.Frame(fare, padding=(10, 0))
                col.pack(side="left")
                ttk.Label(col, text=nombre, font=("Segoe UI", 10, "bold")).pack()
                ttk.Label(col, text=f"${precio:,.2f}", foreground="#0f4c9b", font=("Segoe UI", 12, "bold")).pack()

            # Selector de opción
            ttk.Radiobutton(
                card,
                text="Seleccionar esta opción",
                variable=self.index_var,
                value=i,
            ).pack(anchor="e", pady=(8, 0))

        # Guardar el orden aplicado para continuidad
        self.app_state["opciones_ordenadas"] = opciones

    def _continuar(self):
        idx = self.index_var.get()
        opciones = self.app_state.get("opciones_ordenadas") or self.app_state.get("opciones", [])

        if idx < 0 or idx >= len(opciones):
            messagebox.showwarning("Selección requerida", "Selecciona una opción para continuar")
            return

        self.app_state["opcion_elegida"] = opciones[idx]
        self.on_next()
