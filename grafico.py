from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ui.pantallas.pantalla_busqueda import PantallaBusqueda
from ui.pantallas.pantalla_opciones import PantallaOpciones
from ui.pantallas.pantalla_datos import PantallaDatosPasajero


class FlujoAeroIbero(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AeroIbero - Flujo de reservación")
        self.geometry("1100x720")
        self.minsize(980, 640)

        self.app_state = {}

        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        self.frames = {
            "busqueda": PantallaBusqueda(container, self.app_state, on_next=lambda: self.mostrar("opciones")),
            "opciones": PantallaOpciones(
                container,
                self.app_state,
                on_back=lambda: self.mostrar("busqueda"),
                on_next=lambda: self.mostrar("datos"),
            ),
            "datos": PantallaDatosPasajero(container, self.app_state, on_back=lambda: self.mostrar("opciones")),
        }

        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.mostrar("busqueda")

    def mostrar(self, nombre: str):
        frame = self.frames[nombre]

        # refresca contenido según flujo
        if nombre == "opciones":
            frame.refrescar()

        frame.tkraise()


def run_grafico():
    app = FlujoAeroIbero()
    app.mainloop()


if __name__ == "__main__":
    run_grafico()
