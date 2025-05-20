from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tipos.tipo_sangre import TipoSangre


class RegistroBaseApp:
    """
    Clase base para todas las pantallas de registro de pacientes en el sistema INCUCAI.
    """
    def __init__(self, root, incucai, titulo="Registro de Paciente", tamano="600x650"):
        self.root = root
        self.incucai = incucai
        self.root.title(titulo)
        self.root.geometry(tamano)
        self.root.resizable(False, False)
        
        # Configuración de estilo común
        self.configurar_estilo()
        
        # Frame principal
        self.main_frame = ttk.Frame(root, padding=20, style="Card.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(self.main_frame, text=titulo, style="Header.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, 20), sticky="n")
        
        # Creación de los campos base (común a todas las subclases)
        self.crear_campos_base()
    
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 11), background="#f2f2f2")
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TEntry", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#f2f2f2", foreground="#333")
        style.map("TButton", background=[('active', '#cce5ff')])
        style.configure("Card.TFrame", background="white", relief="groove", borderwidth=1)
        style.configure("Accent.TButton", foreground="white", background="#007acc")
        style.map("Accent.TButton", background=[("active", "#005f99"), ("pressed", "#004c7a")])
    
    def crear_campos_base(self):
        """Crea los campos comunes a todos los registros"""
        # Nombre
        ttk.Label(self.main_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.nombre_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # DNI
        ttk.Label(self.main_frame, text="DNI:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dni_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.dni_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Fecha de nacimiento
        ttk.Label(self.main_frame, text="Fecha de Nacimiento:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.fecha_nac = DateEntry(self.main_frame, width=27, background='darkblue', 
                                  foreground='white', date_pattern='dd/mm/yyyy')
        self.fecha_nac.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Sexo
        ttk.Label(self.main_frame, text="Sexo:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.sexo_var = tk.StringVar()
        sexo_combo = ttk.Combobox(self.main_frame, textvariable=self.sexo_var, width=27)
        sexo_combo['values'] = ['femenino', 'masculino']
        sexo_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        sexo_combo.current(0)
        
        # Número de teléfono
        ttk.Label(self.main_frame, text="Número de Teléfono:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.telefono_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.telefono_var, width=30).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Tipo de sangre
        ttk.Label(self.main_frame, text="Tipo de Sangre:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.sangre_var = tk.StringVar()
        sangre_combo = ttk.Combobox(self.main_frame, textvariable=self.sangre_var, width=27)
        sangre_combo['values'] = [tipo.value for tipo in TipoSangre]
        sangre_combo.grid(row=6, column=1, sticky=tk.W, pady=5)
        sangre_combo.current(0)
        
        # Centro de salud
        ttk.Label(self.main_frame, text="Centro de Salud:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.centro_var = tk.StringVar()
        self.centro_combo = ttk.Combobox(self.main_frame, textvariable=self.centro_var, width=27)
        self.update_centro_combo()
        self.centro_combo.grid(row=7, column=1, sticky=tk.W, pady=5)
    
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
            messagebox.showerror("Error", "Por favor, ingrese un nombre válido.")
            return False
        
        # Validar DNI
        try:
            dni = int(self.dni_var.get().strip())
            if dni <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un DNI válido (número entero positivo).")
            return False
        
        # Validar teléfono
        try:
            telefono = int(self.telefono_var.get().strip())
            if telefono <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número de teléfono válido (número entero positivo).")
            return False
        
        # Validar que haya un centro de salud seleccionado
        if not self.centro_var.get():
            messagebox.showerror("Error", "Por favor, seleccione un centro de salud.")
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
    
    def agregar_botones(self, row, command_registrar, command_limpiar=None):
        """Agrega los botones estándar de registro y limpieza
        
        Args:
            row: Fila donde se colocarán los botones
            command_registrar: Función a ejecutar al presionar el botón de registrar
            command_limpiar: Función a ejecutar al presionar el botón de limpiar (opcional)
        """
        if command_limpiar is None:
            command_limpiar = self.clear_fields_base
            
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Registrar", 
                  command=command_registrar, 
                  style="Accent.TButton").grid(row=0, column=0, padx=10)
        
        ttk.Button(button_frame, text="Limpiar", 
                  command=command_limpiar).grid(row=0, column=1, padx=10)
    
    def crear_frame_fecha_hora(self, parent, label_text, row, var_hora=None, var_minuto=None):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        fecha_frame = ttk.Frame(parent)
        fecha_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        date_entry = DateEntry(fecha_frame, width=15, background='darkblue',
                             foreground='white', date_pattern='dd/mm/yyyy')
        date_entry.pack(side=tk.LEFT)
        
        if var_hora is None:
            var_hora = tk.StringVar(value="00")
        if var_minuto is None:
            var_minuto = tk.StringVar(value="00")
            
        ttk.Label(fecha_frame, text=" Hora: ").pack(side=tk.LEFT)
        hora_spin = ttk.Spinbox(fecha_frame, from_=0, to=23, width=2, 
                               textvariable=var_hora, format="%02.0f")
        hora_spin.pack(side=tk.LEFT)
        
        ttk.Label(fecha_frame, text=":").pack(side=tk.LEFT)
        minuto_spin = ttk.Spinbox(fecha_frame, from_=0, to=59, width=2, 
                                 textvariable=var_minuto, format="%02.0f")
        minuto_spin.pack(side=tk.LEFT)
        
        return date_entry, var_hora, var_minuto
    
    def crear_checkbuttons_organos(self, parent, row, tipos_organo, titulo="Órganos para Donar:", 
                                  organs_per_column=5):
        ttk.Label(parent, text=titulo).grid(row=row, column=0, sticky=tk.NW, pady=5)
        
        # Frame para contener los checkbuttons de órganos
        organos_frame = ttk.Frame(parent)
        organos_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
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
            chk.grid(row=row_pos, column=col, sticky=tk.W, padx=(0 if col == 0 else 10))
            
        return organ_vars
    
    def get_datetime_from_widgets(self, date_entry, hora_var, minuto_var):
        fecha_str = date_entry.get()
        hora = int(hora_var.get())
        minuto = int(minuto_var.get())
        return datetime.strptime(f"{fecha_str} {hora:02d}:{minuto:02d}", "%d/%m/%Y %H:%M")