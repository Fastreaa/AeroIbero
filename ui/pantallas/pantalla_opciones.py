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
        ttk.Label(self, text="2) Elige la mejor opción", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))

        self.info = tk.Text(self, height=14, wrap="word")
        self.info.pack(fill="both", expand=True)

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(10, 0))
        ttk.Button(actions, text="Atrás", command=self.on_back).pack(side="left")
        ttk.Button(actions, text="Continuar", command=self._continuar).pack(side="right")

        self.radio_frame = ttk.Frame(self)
        self.radio_frame.pack(fill="x", pady=(8, 0))

    def refrescar(self):
        for w in self.radio_frame.winfo_children():
            w.destroy()

        opciones = self.app_state.get("opciones", [])
        self.index_var.set(0 if opciones else -1)

        self.info.delete("1.0", tk.END)

        for i, op in enumerate(opciones):
            ttk.Radiobutton(
                self.radio_frame,
                text=f"{op['nombre']} - ${op['costo_total']}",
                variable=self.index_var,
                value=i,
            ).pack(anchor="w")

            self.info.insert(
                tk.END,
                f"[{i+1}] {op['nombre']}\n"
                f"  Criterio: {op['criterio']}\n"
                f"  Ruta: {' -> '.join(op['camino'])}\n"
                f"  Total: ${op['costo_total']}\n\n"
            )

    def _continuar(self):
        idx = self.index_var.get()
        opciones = self.app_state.get("opciones", [])
        if idx < 0 or idx >= len(opciones):
            messagebox.showwarning("Selección requerida", "Selecciona una opción para continuar")
            return

        self.app_state["opcion_elegida"] = opciones[idx]
        self.on_next()
