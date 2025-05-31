from abc import ABC
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from io import StringIO



class ListaCentros(ABC):

    
    def __init__(self):
        if type(self) is ListaCentros:
            raise TypeError(
                "ListaCentros es una clase abstracta y no puede ser instanciada directamente."
            )
        super().__init__()

    def seleccionar_centro(self, centros):
        """
        Muestra una ventana emergente para seleccionar un centro de salud
        """
        # Crear ventana emergente
        popup = tk.Toplevel()
        popup.title("Seleccionar Centro de Salud")
        popup.geometry("400x300")
        popup.resizable(False, False)
        popup.grab_set()  # Hacer modal

        # Centrar la ventana
        popup.transient(self.master if hasattr(self, "master") else None)

        centro_seleccionado = None

        # Título
        titulo = tk.Label(
            popup, text="Seleccione un Centro de Salud", font=("Arial", 12, "bold")
        )
        titulo.pack(pady=10)

        # Frame para la lista
        frame_lista = tk.Frame(popup)
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

        # Listbox con scrollbar
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            frame_lista, yscrollcommand=scrollbar.set, font=("Arial", 10)
        )
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # Agregar centros a la lista
        for centro in centros:
            listbox.insert(tk.END, centro.nombre)

        def on_seleccionar():
            nonlocal centro_seleccionado
            seleccion = listbox.curselection()
            if seleccion:
                centro_seleccionado = centros[seleccion[0]]
                popup.destroy()
            else:
                messagebox.showwarning(
                    "Selección requerida", "Por favor seleccione un centro."
                )

        def on_cancelar():
            popup.destroy()

        # Frame para botones
        frame_botones = tk.Frame(popup)
        frame_botones.pack(pady=10)

        btn_seleccionar = tk.Button(
            frame_botones,
            text="Seleccionar",
            command=on_seleccionar,
            bg="#4CAF50",
            fg="black",
            font=("Arial", 10),
        )
        btn_seleccionar.pack(side="left", padx=10)

        btn_cancelar = tk.Button(
            frame_botones,
            text="Cancelar",
            command=on_cancelar,
            bg="#f44336",
            fg="black",
            font=("Arial", 10),
        )
        btn_cancelar.pack(side="left", padx=10)

        # Permitir doble clic para seleccionar
        listbox.bind("<Double-Button-1>", lambda e: on_seleccionar())

        # Esperar hasta que se cierre la ventana
        popup.wait_window()

        return centro_seleccionado

    def capturar_salida_incucai(self, centro):
        """
        Captura la salida del método mostrar_receptores_por_centro de INCUCAI
        """
        # Capturar stdout
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            # Llamar al método de INCUCAI
            self.incucai.mostrar_receptores_por_centro(centro)

            # Obtener la salida capturada
            output = captured_output.getvalue()

        finally:
            # Restaurar stdout original
            sys.stdout = original_stdout

        return output

    def mostrar_salida(self, salida_texto):
        """
        Muestra la salida capturada de INCUCAI en una ventana emergente
        """
        # Crear ventana emergente
        popup = tk.Toplevel()
        popup.title("Lista de Espera del Centro")
        popup.geometry("500x400")
        popup.resizable(True, True)
        popup.grab_set()  # Hacer modal

        # Centrar la ventana
        popup.transient(self.master if hasattr(self, "master") else None)

        # Frame principal
        frame_principal = tk.Frame(popup)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Área de texto con scrollbar
        frame_texto = tk.Frame(frame_principal)
        frame_texto.pack(fill="both", expand=True)

        # Scrollbars
        scrollbar_v = tk.Scrollbar(frame_texto)
        scrollbar_v.pack(side="right", fill="y")

        scrollbar_h = tk.Scrollbar(frame_texto, orient="horizontal")
        scrollbar_h.pack(side="bottom", fill="x")

        # Text widget
        texto = tk.Text(
            frame_texto,
            yscrollcommand=scrollbar_v.set,
            xscrollcommand=scrollbar_h.set,
            font=("Courier", 10),
            bg="white",
            fg="black",
            wrap="none",
        )
        texto.pack(side="left", fill="both", expand=True)

        # Configurar scrollbars
        scrollbar_v.config(command=texto.yview)
        scrollbar_h.config(command=texto.xview)

        # Insertar el texto capturado
        texto.insert("1.0", salida_texto)
        texto.config(state="disabled")  # Solo lectura

        # Botón cerrar
        btn_cerrar = tk.Button(
            popup,
            text="Cerrar",
            command=popup.destroy,
            bg="#2196F3",
            fg="black",
            font=("Arial", 10),
        )
        btn_cerrar.pack(pady=10)
