from abc import ABC
import tkinter as tk
from tkinter import ttk, messagebox


class EstadoIncucai(ABC):
    def __init__(self):
        if type(self) is EstadoIncucai:
            raise TypeError(
                "EstadoIncucai es una clase abstracta y no puede ser instanciada directamente."
            )
        super().__init__()

    def mostrar_str(self, texto_str):
        """
        Muestra el contenido del __str__ de INCUCAI en una ventana emergente
        """
        # Crear ventana emergente
        popup = tk.Toplevel()
        popup.title("Información del Sistema INCUCAI")
        popup.geometry("700x500")
        popup.resizable(True, True)
        popup.grab_set()  # Hacer modal

        # Centrar la ventana
        popup.transient(self.master if hasattr(self, "master") else None)

        # Frame principal con padding
        frame_principal = tk.Frame(popup)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        titulo = tk.Label(
            frame_principal,
            text="📋 Información del Sistema INCUCAI",
            font=("Arial", 14, "bold"),
            fg="#2c3e50",
        )
        titulo.pack(pady=(0, 15))

        # Frame para el contenido con borde
        frame_contenido = tk.Frame(frame_principal, relief="sunken", bd=2)
        frame_contenido.pack(fill="both", expand=True)

        # Área de texto con scrollbars
        frame_texto = tk.Frame(frame_contenido)
        frame_texto.pack(fill="both", expand=True, padx=2, pady=2)

        # Scrollbar vertical
        scrollbar_v = tk.Scrollbar(frame_texto)
        scrollbar_v.pack(side="right", fill="y")

        # Scrollbar horizontal
        scrollbar_h = tk.Scrollbar(frame_texto, orient="horizontal")
        scrollbar_h.pack(side="bottom", fill="x")

        # Text widget
        texto = tk.Text(
            frame_texto,
            yscrollcommand=scrollbar_v.set,
            xscrollcommand=scrollbar_h.set,
            font=("Courier", 11),
            bg="#f8f9fa",
            fg="#2c3e50",
            wrap="none",
            padx=10,
            pady=10,
            selectbackground="#3498db",
            selectforeground="black",
        )
        texto.pack(side="left", fill="both", expand=True)

        # Configurar scrollbars
        scrollbar_v.config(command=texto.yview)
        scrollbar_h.config(command=texto.xview)

        # Insertar el texto del __str__
        texto.insert("1.0", texto_str)
        texto.config(state="disabled")  # Solo lectura

        # Frame para botones
        frame_botones = tk.Frame(frame_principal)
        frame_botones.pack(fill="x", pady=(15, 0))

        # Botón para copiar al portapapeles
        def copiar_al_portapapeles():
            popup.clipboard_clear()
            popup.clipboard_append(texto_str)
            messagebox.showinfo("Copiado", "Información copiada al portapapeles")

        btn_copiar = tk.Button(
            frame_botones,
            text="📋 Copiar",
            command=copiar_al_portapapeles,
            bg="#17a2b8",
            fg="black",
            font=("Arial", 10),
            relief="flat",
            padx=20,
        )
        btn_copiar.pack(side="left")

        # Botón cerrar
        btn_cerrar = tk.Button(
            frame_botones,
            text="✖ Cerrar",
            command=popup.destroy,
            bg="#dc3545",
            fg="black",
            font=("Arial", 10),
            relief="flat",
            padx=20,
        )
        btn_cerrar.pack(side="right")

        # Información adicional en la parte inferior
        info_label = tk.Label(
            frame_principal,
            text="💡 Esta información muestra el estado actual del sistema INCUCAI",
            font=("Arial", 9, "italic"),
            fg="#6c757d",
        )
        info_label.pack(pady=(10, 0))

        # Atajos de teclado
        popup.bind("<Control-c>", lambda e: copiar_al_portapapeles())
        popup.bind("<Escape>", lambda e: popup.destroy())

        # Focus en la ventana
        popup.focus_set()
