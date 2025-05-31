import tkinter as tk
from .ventana import Ventana
from tkinter import ttk
from abc import ABC



class MostrarMatch(ABC):

    
    def __init__(self):
        if type(self) is MostrarMatch:
            raise TypeError(
                "MostrarMatch es una clase abstracta y no puede ser instanciada directamente."
            )
        super().__init__()

    def mostrar_match(self, resultado):
        """Muestra los resultados del matching en una ventana"""
        window = Ventana.crear_ventana_modal(
            self.root, "🔗 Resultado del Match", "500x400"
        )

        # Header
        ttk.Label(window, text="🔗 Resultado del Match", style="Subheader.TLabel").pack(
            pady=(15, 10)
        )

        # Contenido
        text_box = tk.Text(
            window,
            wrap="word",
            font=("Consolas", 11),
            bg="#ffffff",
            fg="#2c3e50",
            padx=15,
            pady=15,
        )
        text_box.pack(expand=True, fill="both", padx=15, pady=(0, 15))

        # Insertar resultado
        if resultado.strip():
            text_box.insert("1.0", resultado)
        else:
            text_box.insert(
                "1.0", "ℹ️ No se encontraron matches disponibles en este momento."
            )

        text_box.configure(state="disabled")
