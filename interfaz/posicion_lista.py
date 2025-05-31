from abc import ABC
import tkinter as tk
from tkinter import ttk, messagebox
import io
import sys
from io import StringIO
 
class PosicionLista(ABC):
    def __init__(self):
        if type(self) is PosicionLista:
            raise TypeError("PosicionLista es una clase abstracta y no puede ser instanciada directamente.")
        super().__init__()

    def seleccionar_receptor(self, receptores):
        """
        Muestra una ventana emergente para seleccionar un receptor
        """
        # Crear ventana emergente
        popup = tk.Toplevel()
        popup.title("Seleccionar Receptor")
        popup.geometry("450x350")
        popup.resizable(False, False)
        popup.grab_set()  # Hacer modal
        
        # Centrar la ventana
        popup.transient(self.master if hasattr(self, 'master') else None)
        
        receptor_seleccionado = None
        
        # Título
        titulo = tk.Label(popup, text="Seleccione un Receptor", 
                        font=("Arial", 12, "bold"))
        titulo.pack(pady=10)
        
        # Frame para búsqueda
        frame_busqueda = tk.Frame(popup)
        frame_busqueda.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame_busqueda, text="Buscar:", font=("Arial", 10)).pack(side="left")
        entrada_busqueda = tk.Entry(frame_busqueda, font=("Arial", 10))
        entrada_busqueda.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Frame para la lista
        frame_lista = tk.Frame(popup)
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Listbox con scrollbar
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, 
                            font=("Arial", 10))
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Lista original de receptores para filtrado
        receptores_originales = receptores[:]
        
        def actualizar_lista(filtro=""):
            """Actualiza la lista según el filtro de búsqueda"""
            listbox.delete(0, tk.END)
            receptores_filtrados = []
            
            for receptor in receptores_originales:
                if filtro.lower() in receptor.nombre.lower():
                    receptores_filtrados.append(receptor)
                    listbox.insert(tk.END, receptor.nombre)
            
            return receptores_filtrados
        
        # Inicializar lista completa
        receptores_actuales = actualizar_lista()
        
        def on_buscar(*args):
            """Función para filtrar en tiempo real"""
            nonlocal receptores_actuales
            filtro = entrada_busqueda.get()
            receptores_actuales = actualizar_lista(filtro)
        
        # Bind para búsqueda en tiempo real
        entrada_busqueda.bind('<KeyRelease>', on_buscar)
        
        def on_seleccionar():
            nonlocal receptor_seleccionado
            seleccion = listbox.curselection()
            if seleccion:
                receptor_seleccionado = receptores_actuales[seleccion[0]]
                popup.destroy()
            else:
                messagebox.showwarning("Selección requerida", "Por favor seleccione un receptor.")
        
        def on_cancelar():
            popup.destroy()
        
        # Frame para botones
        frame_botones = tk.Frame(popup)
        frame_botones.pack(pady=10)
        
        btn_seleccionar = tk.Button(frame_botones, text="Consultar Posición", 
                                command=on_seleccionar, bg="#4CAF50", 
                                fg="black", font=("Arial", 10))
        btn_seleccionar.pack(side="left", padx=10)
        
        btn_cancelar = tk.Button(frame_botones, text="Cancelar", 
                                command=on_cancelar, bg="#f44336", 
                                fg="black", font=("Arial", 10))
        btn_cancelar.pack(side="left", padx=10)
        
        # Permitir doble clic para seleccionar
        listbox.bind("<Double-Button-1>", lambda e: on_seleccionar())
        
        # Focus en el campo de búsqueda
        entrada_busqueda.focus()
        
        # Esperar hasta que se cierre la ventana
        popup.wait_window()
        
        return receptor_seleccionado

    def capturar_salida_prioridad(self, receptor):
        """
        Captura la salida del método mostrar_prioridad_receptor de INCUCAI
        """
        # Capturar stdout
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            # Llamar al método de INCUCAI
            self.incucai.mostrar_prioridad_receptor(receptor)
            
            # Obtener la salida capturada
            output = captured_output.getvalue()
            
        finally:
            # Restaurar stdout original
            sys.stdout = original_stdout
        
        return output

    def mostrar_posicion(self, salida_texto):
        """
        Muestra la posición del receptor en una ventana emergente
        """
        # Crear ventana emergente
        popup = tk.Toplevel()
        popup.title("Posición en Lista de Espera")
        popup.geometry("400x200")
        popup.resizable(False, False)
        popup.grab_set()  # Hacer modal
        
        # Centrar la ventana
        popup.transient(self.master if hasattr(self, 'master') else None)
        
        # Frame principal
        frame_principal = tk.Frame(popup)
        frame_principal.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Icono y mensaje principal
        frame_mensaje = tk.Frame(frame_principal)
        frame_mensaje.pack(expand=True)
        
        # Determinar si está en la lista o no
        if "no está en la lista de espera" in salida_texto:
            # Receptor no está en la lista
            icono = "❌"
            color_fondo = "#ffebee"
            color_texto = "#c62828"
        else:
            # Receptor está en la lista
            icono = "📍"
            color_fondo = "#e8f5e8"
            color_texto = "#2e7d32"
        
        # Configurar fondo de la ventana
        popup.configure(bg=color_fondo)
        frame_principal.configure(bg=color_fondo)
        frame_mensaje.configure(bg=color_fondo)
        
        # Mostrar el icono
        label_icono = tk.Label(frame_mensaje, text=icono, 
                            font=("Arial", 24), 
                            bg=color_fondo)
        label_icono.pack(pady=(0, 10))
        
        # Mostrar el mensaje (sin saltos de línea innecesarios)
        mensaje_limpio = salida_texto.strip()
        label_mensaje = tk.Label(frame_mensaje, text=mensaje_limpio,
                                font=("Arial", 12),
                                fg=color_texto,
                                bg=color_fondo,
                                wraplength=350,
                                justify="center")
        label_mensaje.pack()
        
        # Botón cerrar
        btn_cerrar = tk.Button(popup, text="Cerrar", command=popup.destroy, 
                            bg="#2196F3", fg="black", font=("Arial", 10))
        btn_cerrar.pack(pady=20)