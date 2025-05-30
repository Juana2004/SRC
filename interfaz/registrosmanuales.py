import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import io
import sys
from io import StringIO

from sistema.match import Match
from .registroreceptor import RegistroReceptorApp
from .registrodonante import RegistroDonanteApp
from .registrodonantevivo import RegistroDonanteVivoApp
from .formato_lista import FormatoListaDeEspera
from .salida_metodos import SalidaMetodos
from .ventana import Ventana

class IncucaiApp:

    def __init__(self, root, incucai):
        self.root = root
        self.incucai = incucai
        
        self._setup_main_window()
        self._create_main_interface()
    
    def _setup_main_window(self):
        """Configura la ventana principal"""
        self.root.title("🏥 Sistema INCUCAI - Gestión de Trasplantes")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg= '#ecf0f1')
        
        # Centrar ventana
        width, height = map(int, "900x700".split('x'))
        Ventana.centrar_ventana(self.root, width, height)
    
    def _create_main_interface(self):
        """Crea la interfaz principal"""
        main_frame = ttk.Frame(self.root, padding=30, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self._create_header(main_frame)
        self._create_description(main_frame)
        self._create_action_buttons(main_frame)
    
    def _create_header(self, parent):
        """Crea el encabezado de la aplicación"""
        ttk.Label(
            parent,
            text="🏥 Sistema de Gestión INCUCAI",
            style="Header.TLabel"
        ).pack(pady=(0, 20))
    
    def _create_description(self, parent):
        """Crea la descripción de la aplicación"""
        description = (
            "Sistema integral para la gestión de donantes, receptores\n"
            "y coordinación de trasplantes de órganos"
        )
        
        ttk.Label(
            parent,
            text=description,
            wraplength=500,
            justify="center",
            style="Info.TLabel"
        ).pack(pady=(0, 30))
    
    def _create_action_buttons(self, parent):
        """Crea los botones de acción principales"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, expand=True)
        
        buttons_config = [
            (" Estado Actual", self.mostrar_str_incucai, "Primary.TButton"),
            (" Registrar Receptor", self.open_receptor_form, "TButton"),
            (" Registrar Donante", self.open_donante_form, "TButton"),
            (" Registrar Donante Vivo", self.open_donante_vivo_form, "TButton"),
            (" Realizar Match", self.realizar_match, "TButton"),
            (" Ver lista de espera de un centro", self.mostrar_lista_espera_centro, "TButton"),
            (" Ver posicion de receptor en lista de espera", self.mostrar_posicion_receptor_espera, "TButton")

        ]
        
        for text, command, style in buttons_config:
            ttk.Button(
                button_frame,
                text=text,
                command=command,
                width=30,
                style=style
            ).pack(pady=8)
    
    # Métodos para abrir formularios



    def mostrar_str_incucai(self):
        """
        Método para mostrar el __str__ de INCUCAI en una ventana emergente
        """
        try:
            # Obtener la representación string de INCUCAI
            str_incucai = str(self.incucai)
            
            # Mostrar en ventana emergente
            self.mostrar_str_popup(str_incucai)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar información de INCUCAI: {e}")

    def mostrar_str_popup(self, texto_str):
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
        popup.transient(self.master if hasattr(self, 'master') else None)
        
        # Frame principal con padding
        frame_principal = tk.Frame(popup)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(frame_principal, 
                        text="📋 Información del Sistema INCUCAI", 
                        font=("Arial", 14, "bold"),
                        fg="#2c3e50")
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
        texto = tk.Text(frame_texto, 
                    yscrollcommand=scrollbar_v.set,
                    xscrollcommand=scrollbar_h.set,
                    font=("Courier", 11),
                    bg="#f8f9fa",
                    fg="#2c3e50",
                    wrap="none",
                    padx=10,
                    pady=10,
                    selectbackground="#3498db",
                    selectforeground="black")
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
        
        btn_copiar = tk.Button(frame_botones, 
                            text="📋 Copiar", 
                            command=copiar_al_portapapeles,
                            bg="#17a2b8", 
                            fg="black", 
                            font=("Arial", 10),
                            relief="flat",
                            padx=20)
        btn_copiar.pack(side="left")
        
        # Botón cerrar
        btn_cerrar = tk.Button(frame_botones, 
                            text="✖ Cerrar", 
                            command=popup.destroy, 
                            bg="#dc3545", 
                            fg="black", 
                            font=("Arial", 10),
                            relief="flat",
                            padx=20)
        btn_cerrar.pack(side="right")
        
        # Información adicional en la parte inferior
        info_label = tk.Label(frame_principal, 
                            text="💡 Esta información muestra el estado actual del sistema INCUCAI",
                            font=("Arial", 9, "italic"),
                            fg="#6c757d")
        info_label.pack(pady=(10, 0))
        
        # Atajos de teclado
        popup.bind('<Control-c>', lambda e: copiar_al_portapapeles())
        popup.bind('<Escape>', lambda e: popup.destroy())
        
        # Focus en la ventana
        popup.focus_set()

    def mostrar_posicion_receptor_espera(self):
        """
        Método para manejar el botón 'Ver posición de receptor en lista de espera'
        Permite seleccionar un receptor y ver su posición en la lista de espera
        """
        try:
            # Obtener lista de receptores disponibles
            receptores = self.incucai.receptores  # Asumiendo que existe este método
            
            if not receptores:
                messagebox.showwarning("Sin receptores", "No hay receptores registrados.")
                return
            
            # Crear ventana para seleccionar receptor
            receptor_seleccionado = self.seleccionar_receptor_popup(receptores)
            
            if receptor_seleccionado:
                # Capturar la salida del método de INCUCAI
                salida_capturada = self.capturar_salida_prioridad_incucai(receptor_seleccionado)
                
                # Mostrar la salida en ventana emergente
                self.mostrar_posicion_popup(salida_capturada)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al consultar posición del receptor: {e}")

    def seleccionar_receptor_popup(self, receptores):
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

    def capturar_salida_prioridad_incucai(self, receptor):
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

    def mostrar_posicion_popup(self, salida_texto):
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
        
    def mostrar_lista_espera_centro(self):
        """
        Método para manejar el botón 'Mostrar lista de espera de un centro'
        Muestra ventanas emergentes para seleccionar centro y ver receptores
        """
        try:
            # Obtener lista de centros disponibles
            centros = self.incucai.centros_salud
            
            if not centros:
                messagebox.showwarning("Sin centros", "No hay centros de salud registrados.")
                return
            
            # Crear ventana para seleccionar centro
            centro_seleccionado = self.seleccionar_centro_popup(centros)
            
            if centro_seleccionado:
                # Capturar la salida del método de INCUCAI
                salida_capturada = self.capturar_salida_incucai(centro_seleccionado)
                
                # Mostrar la salida en ventana emergente
                self.mostrar_salida_popup(salida_capturada)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la lista de espera: {e}")

    def seleccionar_centro_popup(self, centros):
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
        popup.transient(self.master if hasattr(self, 'master') else None)
        
        centro_seleccionado = None
        
        # Título
        titulo = tk.Label(popup, text="Seleccione un Centro de Salud", 
                        font=("Arial", 12, "bold"))
        titulo.pack(pady=10)
        
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
                messagebox.showwarning("Selección requerida", "Por favor seleccione un centro.")
        
        def on_cancelar():
            popup.destroy()
        
        # Frame para botones
        frame_botones = tk.Frame(popup)
        frame_botones.pack(pady=10)
        
        btn_seleccionar = tk.Button(frame_botones, text="Seleccionar", 
                                command=on_seleccionar, bg="#4CAF50", 
                                fg="black", font=("Arial", 10))
        btn_seleccionar.pack(side="left", padx=10)
        
        btn_cancelar = tk.Button(frame_botones, text="Cancelar", 
                                command=on_cancelar, bg="#f44336", 
                                fg="black", font=("Arial", 10))
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

    def mostrar_salida_popup(self, salida_texto):
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
        popup.transient(self.master if hasattr(self, 'master') else None)
        
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
        texto = tk.Text(frame_texto, 
                    yscrollcommand=scrollbar_v.set,
                    xscrollcommand=scrollbar_h.set,
                    font=("Courier", 10),
                    bg="white",
                    fg="black",
                    wrap="none")
        texto.pack(side="left", fill="both", expand=True)
        
        # Configurar scrollbars
        scrollbar_v.config(command=texto.yview)
        scrollbar_h.config(command=texto.xview)
        
        # Insertar el texto capturado
        texto.insert("1.0", salida_texto)
        texto.config(state="disabled")  # Solo lectura
        
        # Botón cerrar
        btn_cerrar = tk.Button(popup, text="Cerrar", command=popup.destroy, 
                            bg="#2196F3", fg="black", font=("Arial", 10))
        btn_cerrar.pack(pady=10)

    # Método auxiliar si no existe
    def obtener_centros_salud(self):
        """
        Método auxiliar para obtener la lista de centros de salud
        Debes implementar según tu estructura de datos
        """
        # Ejemplo de implementación - ajustar según tu código
        # return self.centros  # o como tengas almacenados los centros
        pass


    def open_receptor_form(self):
        """Abre el formulario de registro de receptor"""
        receptor_window = tk.Toplevel(self.root)
        RegistroReceptorApp(receptor_window, self.incucai)
        receptor_window.transient(self.root)
    
    def open_donante_form(self):
        """Abre el formulario de registro de donante"""
        donante_window = tk.Toplevel(self.root)
        RegistroDonanteApp(donante_window, self.incucai)
        donante_window.transient(self.root)
    
    def open_donante_vivo_form(self):
        """Abre el formulario de registro de donante vivo"""
        donante_vivo_window = tk.Toplevel(self.root)
        RegistroDonanteVivoApp(donante_vivo_window, self.incucai)
        donante_vivo_window.transient(self.root)
    
    def realizar_match(self):
        """Ejecuta el algoritmo de matching y muestra resultados"""
        with SalidaMetodos() as capture:
            try:
                match_instance = Match(self.incucai)
                match_instance.match()
            except Exception as e:
                print(f"Error en el proceso de matching: {str(e)}")
        
        resultado = capture.get_output()
        self._show_match_results(resultado)
    
    def _show_match_results(self, resultado):
        """Muestra los resultados del matching en una ventana"""
        window = Ventana.crear_ventana_modal(
            self.root,
            "🔗 Resultado del Match",
            "500x400"
        )
        
        # Header
        ttk.Label(
            window,
            text="🔗 Resultado del Match",
            style="Subheader.TLabel"
        ).pack(pady=(15, 10))
        
        # Contenido
        text_box = tk.Text(
            window,
            wrap="word",
            font=("Consolas", 11),
            bg= '#ffffff',
            fg='#2c3e50',
            padx=15,
            pady=15
        )
        text_box.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        
        # Insertar resultado
        if resultado.strip():
            text_box.insert("1.0", resultado)
        else:
            text_box.insert("1.0", "ℹ️ No se encontraron matches disponibles en este momento.")
        
        text_box.configure(state="disabled")
    
    def mostrar_lista_de_espera(self):
        """Muestra la lista de espera en una ventana dedicada"""
        with SalidaMetodos() as capture:
            try:
                self.incucai.mostrar_lista_de_espera()
            except Exception as e:
                print(f"Error al obtener lista de espera: {str(e)}")
        
        resultado = capture.get_output()
        self._create_wait_list_window(resultado)
    
    def _create_wait_list_window(self, content):
        """Crea la ventana de lista de espera"""
        window = Ventana.crear_ventana_modal(
            self.root,
            "📋 Lista de Espera - INCUCAI",
            "900x700"
        )
        
        main_frame = ttk.Frame(window, padding=25)
        main_frame.pack(fill="both", expand=True)
        
        self._create_wait_list_header(main_frame, content)
        self._create_wait_list_content(main_frame, content)
        self._create_wait_list_controls(main_frame, window, content)
        
        # Atajos de teclado
        window.bind('<Escape>', lambda e: window.destroy())
        window.bind('<Control-s>', lambda e: self._export_wait_list(window, content))
        
        window.focus_set()
    
    def _create_wait_list_header(self, parent, content):
        """Crea el encabezado de la lista de espera"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título
        ttk.Label(
            header_frame,
            text="📋 Lista de Espera",
            style="Subheader.TLabel"
        ).pack(side="left")
        
        # Información estadística
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill="x", pady=(0, 15))
        
        patient_count = FormatoListaDeEspera.count_patients(content)
        timestamp = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        
        ttk.Label(
            info_frame,
            text=f"👥 Total de pacientes: {patient_count}",
            style="Info.TLabel"
        ).pack(side="left")
        
        ttk.Label(
            info_frame,
            text=f"🕐 Actualizado: {timestamp}",
            style="Info.TLabel"
        ).pack(side="right")
    
    def _create_wait_list_content(self, parent, content):
        """Crea el área de contenido de la lista de espera"""
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Text widget con scrollbars
        text_box = tk.Text(
            text_frame,
            wrap="none",
            font=("Consolas", 11),
            bg='#ffffff',
            fg='#2c3e50',
            selectbackground="white",
            selectforeground="white",
            relief="flat",
            borderwidth=1,
            padx=20,
            pady=20,
            spacing1=3,
            spacing3=3
        )
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_box.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient="horizontal", command=text_box.xview)
        
        text_box.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Layout con grid
        text_box.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        # Insertar contenido formateado
        formatted_content = FormatoListaDeEspera.format_wait_list(content)
        text_box.insert("1.0", formatted_content)
        text_box.configure(state="disabled")
    
    def _create_wait_list_controls(self, parent, window, content):
        """Crea los controles de la ventana de lista de espera"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x")
        
        # Botón exportar
        ttk.Button(
            button_frame,
            text="💾 Exportar (Ctrl+S)",
            command=lambda: self._export_wait_list(window, content)
        ).pack(side="left", padx=(0, 15))
        
        # Botón cerrar
        ttk.Button(
            button_frame,
            text="❌ Cerrar (Esc)",
            command=window.destroy
        ).pack(side="right")
    
   