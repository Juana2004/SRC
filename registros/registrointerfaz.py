'''from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tipos.tipo_sangre import TipoSangre


class RegistroBaseApp:
    """
    Clase base para todas las pantallas de registro de pacientes en el sistema INCUCAI.
    """
    def __init__(self, root, incucai, titulo="Registro de Paciente", tamano="800x700"):
        self.root = root
        self.incucai = incucai
        self.root.title(f"INCUCAI - {titulo}")
        
        # Tamaño fijo y estandarizado para todas las pantallas incluyendo donante
        self.root.geometry(tamano)
        self.root.minsize(700, 820)  # Establece un tamaño mínimo
        self.root.resizable(False, False)
        
        # Colores y estilo médico profesional
        self.COLOR_PRIMARIO = "#1a73e8"  # Azul principal
        self.COLOR_SECUNDARIO = "#4285f4"  # Azul secundario
        self.COLOR_FONDO = "#f8f9fa"  # Gris muy claro/blanco
        self.COLOR_TEXTO = "#202124"  # Gris oscuro para texto
        self.COLOR_ACENTO = "#0d47a1"  # Azul oscuro para acentos
        self.COLOR_ERROR = "#d93025"  # Rojo para errores
        
        # Configuración de estilo médico profesional
        self.configurar_estilo()
        
        # Frame principal con efecto de tarjeta
        self.main_frame = ttk.Frame(root, padding=20, style="Card.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header con logo/título
        self.header_frame = ttk.Frame(self.main_frame, style="Header.TFrame")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Título con ícono médico
        ttk.Label(self.header_frame, text="🏥", font=("Segoe UI", 18), 
                 background=self.COLOR_PRIMARIO, foreground="white").pack(side=tk.LEFT, padx=(5, 0))
        ttk.Label(self.header_frame, text=titulo, style="Header.TLabel").pack(side=tk.LEFT, padx=10)
        
        # Agregar botón de buscar match en el header (a la derecha)
        self.match_button = ttk.Button(self.header_frame, text="Buscar Match 🔍", 
                                      command=self.buscar_match, style="Match.TButton")
        self.match_button.pack(side=tk.RIGHT, padx=10)
        
        # Creación de los campos base (común a todas las subclases)
        self.crear_campos_base()
    
    def configurar_estilo(self):
        """Configura un estilo profesional médico con tonos azules y grises"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilos base
        style.configure("TFrame", background=self.COLOR_FONDO)
        style.configure("TLabel", font=("Segoe UI", 11), background=self.COLOR_FONDO, foreground=self.COLOR_TEXTO)
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=8)
        style.configure("TEntry", font=("Segoe UI", 11), fieldbackground="white", borderwidth=1)
        style.configure("TCombobox", font=("Segoe UI", 11), fieldbackground="white")
        style.configure("TCheckbutton", font=("Segoe UI", 11), background=self.COLOR_FONDO)
        style.configure("TSpinbox", font=("Segoe UI", 11), fieldbackground="white")
        
        # Estilos específicos
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background=self.COLOR_PRIMARIO, foreground="white")
        style.configure("Header.TFrame", background=self.COLOR_PRIMARIO)
        style.configure("Card.TFrame", background="white", relief="ridge", borderwidth=1)
        style.configure("Section.TFrame", background="white", relief="groove", borderwidth=0)
        
        # Botones
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), foreground="white", background=self.COLOR_PRIMARIO)
        style.map("Accent.TButton", 
                 background=[("active", self.COLOR_SECUNDARIO), ("pressed", self.COLOR_ACENTO)],
                 foreground=[("active", "white"), ("pressed", "white")])
                 
        style.configure("Secondary.TButton", font=("Segoe UI", 11), background="#e8eaed")
        style.map("Secondary.TButton", 
                 background=[("active", "#d2d5db"), ("pressed", "#bdc1c6")])
                 
        style.configure("Critical.TButton", font=("Segoe UI", 11, "bold"), foreground="white", background="#ea4335")
        style.map("Critical.TButton", 
                 background=[("active", "#f25545"), ("pressed", "#b31412")])
        
        # Estilo específico para el botón de match
        style.configure("Match.TButton", font=("Segoe UI", 11, "bold"), foreground="white", background="#34a853")
        style.map("Match.TButton", 
                 background=[("active", "#46be64"), ("pressed", "#107c30")],
                 foreground=[("active", "white"), ("pressed", "white")])
    
    def buscar_match(self):
        """Ejecuta el algoritmo de matching y muestra los resultados en una ventana"""
        try:
            # Ejecutar el algoritmo de matching
            resultados = self.incucai.match()
            
            # Crear ventana para mostrar resultados
            match_window = tk.Toplevel(self.root)
            match_window.title("Resultados de Match")
            match_window.geometry("600x400")
            match_window.minsize(600, 400)
            match_window.grab_set()  # Hace modal la ventana
            
            # Frame principal
            main_frame = ttk.Frame(match_window, padding=20, style="Card.TFrame")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            ttk.Label(main_frame, text="Resultados de Match", 
                    font=("Segoe UI", 16, "bold")).grid(row=0, column=0, pady=(0, 20))
            
            # Marco para resultados con scroll
            resultados_frame = ttk.Frame(main_frame, style="Card.TFrame")
            resultados_frame.grid(row=1, column=0, sticky="nsew")
            main_frame.columnconfigure(0, weight=1)
            main_frame.rowconfigure(1, weight=1)
            
            # Crear scrollbar
            scrollbar = ttk.Scrollbar(resultados_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Crear Text widget para mostrar resultados
            resultado_text = tk.Text(resultados_frame, font=("Segoe UI", 11), 
                                    yscrollcommand=scrollbar.set, wrap=tk.WORD)
            resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=resultado_text.yview)
            
            # Insertar resultados en el Text widget
            if resultados:
                for linea in resultados:
                    resultado_text.insert(tk.END, linea + "\n")
            else:
                resultado_text.insert(tk.END, "No se encontraron matches en este momento.")
            
            resultado_text.config(state=tk.DISABLED)  # Hacer el texto de solo lectura
            
            # Botón para cerrar
            ttk.Button(main_frame, text="Cerrar", style="Secondary.TButton",
                    command=match_window.destroy).grid(row=2, column=0, pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar el match: {str(e)}")


    def crear_campos_base(self):
        """Crea los campos comunes a todos los registros con mejor distribución y estética"""
        # Frame para información personal
        info_frame = ttk.LabelFrame(self.main_frame, text="Información Personal", padding=15, style="Section.TFrame")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Primera columna - info básica
        col1 = ttk.Frame(info_frame, style="Section.TFrame")
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Segunda columna - info adicional
        col2 = ttk.Frame(info_frame, style="Section.TFrame")
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # COLUMNA 1
        # Nombre con ícono
        nombre_frame = ttk.Frame(col1, style="Section.TFrame")
        nombre_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        ttk.Label(nombre_frame, text="👤").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(nombre_frame, text="Nombre:").pack(side=tk.LEFT)
        
        self.nombre_var = tk.StringVar()
        ttk.Entry(col1, textvariable=self.nombre_var, width=30).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # DNI con ícono
        dni_frame = ttk.Frame(col1, style="Section.TFrame")
        dni_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        ttk.Label(dni_frame, text="DNI:").pack(side=tk.LEFT)
        
        self.dni_var = tk.StringVar()
        ttk.Entry(col1, textvariable=self.dni_var, width=30).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Fecha de nacimiento
        fecha_frame = ttk.Frame(col1, style="Section.TFrame")
        fecha_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
        ttk.Label(fecha_frame, text="Fecha de Nacimiento:").pack(side=tk.LEFT)
        
        self.fecha_nac = DateEntry(col1, width=28, background=self.COLOR_PRIMARIO, 
                                  foreground='white', date_pattern='dd/mm/yyyy')
        self.fecha_nac.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # COLUMNA 2
        # Sexo con ícono
        sexo_frame = ttk.Frame(col2, style="Section.TFrame")
        sexo_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        ttk.Label(sexo_frame, text="Sexo:").pack(side=tk.LEFT)
        
        self.sexo_var = tk.StringVar()
        sexo_combo = ttk.Combobox(col2, textvariable=self.sexo_var, width=27, state="readonly")
        sexo_combo['values'] = ['femenino', 'masculino']
        sexo_combo.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        sexo_combo.current(0)
        
        # Teléfono con ícono
        tel_frame = ttk.Frame(col2, style="Section.TFrame")
        tel_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        ttk.Label(tel_frame, text="Número de Teléfono:").pack(side=tk.LEFT)
        
        self.telefono_var = tk.StringVar()
        ttk.Entry(col2, textvariable=self.telefono_var, width=30).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Frame para información médica
        med_frame = ttk.LabelFrame(self.main_frame, text="Información Médica", padding=15, style="Section.TFrame")
        med_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Tipo de sangre con ícono
        sangre_frame = ttk.Frame(med_frame, style="Section.TFrame")
        sangre_frame.grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(sangre_frame, text="Tipo de Sangre:").pack(side=tk.LEFT)
        
        self.sangre_var = tk.StringVar()
        sangre_combo = ttk.Combobox(med_frame, textvariable=self.sangre_var, width=27, state="readonly")
        sangre_combo['values'] = [tipo.value for tipo in TipoSangre]
        sangre_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        sangre_combo.current(0)
        
        # Centro de salud con ícono
        centro_frame = ttk.Frame(med_frame, style="Section.TFrame")
        centro_frame.grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(centro_frame, text="Centro de Salud:").pack(side=tk.LEFT)
        
        self.centro_var = tk.StringVar()
        self.centro_combo = ttk.Combobox(med_frame, textvariable=self.centro_var, width=27, state="readonly")
        self.update_centro_combo()
        self.centro_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
    
    def update_centro_combo(self):
        """Actualiza el combobox de centros de salud con los disponibles en INCUCAI"""
        centros = [centro.nombre for centro in self.incucai.centros_salud]
        self.centro_combo['values'] = centros
        if centros:
            self.centro_combo.current(0)
        else:
            self.centro_var.set('')  # Si no hay centro limpio el combo
    
    def validate_fields_base(self):
        """Valida los campos comunes a todos los registros
        
        Returns:
            bool: True si todos los campos son válidos, False en caso contrario
        """
        # Validar nombre
        if not self.nombre_var.get().strip():
            messagebox.showerror("Error de Validación", "Por favor, ingrese un nombre válido.")
            return False
        
        # Validar DNI
        try:
            dni = int(self.dni_var.get().strip())
            if dni <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error de Validación", "Por favor, ingrese un DNI válido (número entero positivo).")
            return False
        
        # Validar teléfono
        try:
            telefono = int(self.telefono_var.get().strip())
            if telefono <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error de Validación", "Por favor, ingrese un número de teléfono válido (número entero positivo).")
            return False
        
        # Validar que haya un centro de salud seleccionado
        if not self.centro_var.get():
            messagebox.showerror("Error de Validación", "Por favor, seleccione un centro de salud.")
            return False
        
        return True
    
    def get_centro_salud(self):
        """Obtiene el objeto centro de salud seleccionado
        
        Returns:
            object: Objeto centro de salud o None si no se encuentra
        """
        centro_nombre = self.centro_var.get()
        for centro in self.incucai.centros_salud:
            if centro.nombre == centro_nombre:
                return centro
        return None
    
    def clear_fields_base(self):
        """Limpia los campos base comunes a todos los registros"""
        self.nombre_var.set("")
        self.dni_var.set("")
        self.fecha_nac.set_date(datetime.now().date())
        self.sexo_var.set("femenino")
        self.telefono_var.set("")
        self.sangre_var.set(TipoSangre.A_POSITIVO.value)
        self.centro_var.set("")
    
    def agregar_botones(self, row, command_registrar, command_limpiar=None, command_cancelar=None):
        """Agrega los botones estándar de registro y limpieza
        
        Args:
            row: Fila donde se colocarán los botones
            command_registrar: Función a ejecutar al presionar el botón de registrar
            command_limpiar: Función a ejecutar al presionar el botón de limpiar (opcional)
            command_cancelar: Función a ejecutar al presionar el botón de cancelar (opcional)
        """
        if command_limpiar is None:
            command_limpiar = self.clear_fields_base
            
        # Frame para botones con ancho completo
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20, sticky="ew")
        
        # Configurar el grid para centrar los botones
        button_frame.columnconfigure(0, weight=1)  # Espacio izquierda
        button_frame.columnconfigure(4, weight=1)  # Espacio derecha
        
        ttk.Button(button_frame, text="Registrar ✓", 
                  command=command_registrar, width=15,
                  style="Accent.TButton").grid(row=0, column=1, padx=10)
        
        ttk.Button(button_frame, text="Limpiar ↺", 
                  command=command_limpiar, width=15,
                  style="Secondary.TButton").grid(row=0, column=2, padx=10)
        
        if command_cancelar:
            ttk.Button(button_frame, text="Cancelar ✕", 
                      command=command_cancelar, width=15,
                      style="Secondary.TButton").grid(row=0, column=3, padx=10)
    
    def crear_frame_fecha_hora(self, parent, label_text, row, var_hora=None, var_minuto=None):
        """Crea un widget compuesto para fecha y hora con mejor estética"""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        fecha_frame = ttk.Frame(parent)
        fecha_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        date_entry = DateEntry(fecha_frame, width=15, background=self.COLOR_PRIMARIO,
                             foreground='white', date_pattern='dd/mm/yyyy')
        date_entry.pack(side=tk.LEFT)
        
        if var_hora is None:
            var_hora = tk.StringVar(value="00")
        if var_minuto is None:
            var_minuto = tk.StringVar(value="00")
            
        # Frame para hora/minutos con borde
        hora_frame = ttk.Frame(fecha_frame, style="Card.TFrame", padding=1)
        hora_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Label(hora_frame, text="Hora:", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        hora_spin = ttk.Spinbox(hora_frame, from_=0, to=23, width=2, 
                               textvariable=var_hora, format="%02.0f")
        hora_spin.pack(side=tk.LEFT)
        
        ttk.Label(hora_frame, text=":").pack(side=tk.LEFT)
        minuto_spin = ttk.Spinbox(hora_frame, from_=0, to=59, width=2, 
                                 textvariable=var_minuto, format="%02.0f")
        minuto_spin.pack(side=tk.LEFT, padx=(0, 5))
        
        return date_entry, var_hora, var_minuto
    
    def crear_checkbuttons_organos(self, parent, row, tipos_organo, titulo="Órganos para Donar:", 
                                  organs_per_column=4):
        """Crea un grupo de checkbuttons para órganos con mejor estética"""
        # Frame contenedor para toda la sección de órganos
        organos_container = ttk.Frame(parent)
        organos_container.grid(row=row, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Título de la sección
        ttk.Label(organos_container, text=titulo, font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(5, 10))
        
        # Frame para contener los checkbuttons de órganos con borde suave
        organos_frame = ttk.Frame(organos_container, style="Card.TFrame")
        organos_frame.grid(row=1, column=0, sticky="ew", pady=5, padx=2)
        
        # Crear variables y checkbuttons para cada tipo de órgano
        organ_vars = {}
        
        # Organizar los checkbuttons en columnas
        for i, organo in enumerate(tipos_organo):
            # Calcular posición en la grid
            col = i // organs_per_column
            row_pos = i % organs_per_column
            
            var = tk.BooleanVar(value=False)
            organ_vars[organo] = var
            
            # Crear y posicionar el checkbutton
            chk = ttk.Checkbutton(organos_frame, text=organo, variable=var)
            chk.grid(row=row_pos, column=col, sticky=tk.W, padx=(15 if col == 0 else 25), pady=5)
            
        return organ_vars
    
    def get_datetime_from_widgets(self, date_entry, hora_var, minuto_var):
        """Convierte widgets de fecha y hora en un objeto datetime"""
        fecha_str = date_entry.get()
        hora = int(hora_var.get())
        minuto = int(minuto_var.get())
        return datetime.strptime(f"{fecha_str} {hora:02d}:{minuto:02d}", "%d/%m/%Y %H:%M")
        
    def mostrar_mensaje_exito(self, mensaje="Registro completado con éxito"):
        """Muestra un mensaje de éxito con estilo mejorado"""
        messagebox.showinfo("Operación Exitosa", mensaje)
        '''