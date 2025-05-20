##TEREEEE ESTEEEEE
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# Importaciones de pacientes
from pacientes.donante import Donante
from datetime import datetime


# Importaciones de tipos
from tipos.tipo_organo import TipoOrgano
from tipos.tipo_sangre import TipoSangre


class RegistroDonantesApp:
    def __init__(self, root, incucai):
        self.root = root
        self.incucai = incucai
        self.root.title("Registro de Donantes")
        self.root.geometry("600x650")
        self.root.resizable(False, False)
        
        # Estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 11), background="#f2f2f2")
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TEntry", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#f2f2f2", foreground="#333")
        style.map("TButton", background=[('active', '#cce5ff')])
        
        # Frame principal
        main_frame = ttk.Frame(root, padding=20, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        style.configure("Card.TFrame", background="white", relief="groove", borderwidth=1)
        
        # Título
        ttk.Label(main_frame, text="Registro de Donantes", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="n")
        
        # Creación de los campos
        self.create_fields(main_frame)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Registrar", command=self.register_donante, style="Accent.TButton").grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_fields).grid(row=0, column=1, padx=10)
        
        style.configure("Accent.TButton", foreground="white", background="#007acc")
        style.map("Accent.TButton",
                 background=[("active", "#005f99"), ("pressed", "#004c7a")])
    
    def create_fields(self, parent):
        # Nombre
        ttk.Label(parent, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.nombre_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # DNI
        ttk.Label(parent, text="DNI:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dni_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.dni_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Fecha de nacimiento
        ttk.Label(parent, text="Fecha de Nacimiento:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.fecha_nac = DateEntry(parent, width=27, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy')
        self.fecha_nac.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Sexo
        ttk.Label(parent, text="Sexo:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.sexo_var = tk.StringVar()
        sexo_combo = ttk.Combobox(parent, textvariable=self.sexo_var, width=27)
        sexo_combo['values'] = ['femenino', 'masculino']
        sexo_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        sexo_combo.current(0)
        
        # Número de teléfono
        ttk.Label(parent, text="Número de Teléfono:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.telefono_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.telefono_var, width=30).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Tipo de sangre
        ttk.Label(parent, text="Tipo de Sangre:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.sangre_var = tk.StringVar()
        sangre_combo = ttk.Combobox(parent, textvariable=self.sangre_var, width=27)
        sangre_combo['values'] = [tipo.value for tipo in TipoSangre]
        sangre_combo.grid(row=6, column=1, sticky=tk.W, pady=5)
        sangre_combo.current(0)
        
        # Centro de salud
        ttk.Label(parent, text="Centro de Salud:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.centro_var = tk.StringVar()
        self.centro_combo = ttk.Combobox(parent, textvariable=self.centro_var, width=27)
        self.update_centro_combo()
        self.centro_combo.grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # Fecha y hora de fallecimiento
        ttk.Label(parent, text="Fecha de Fallecimiento:").grid(row=8, column=0, sticky=tk.W, pady=5)
        fecha_fallec_frame = ttk.Frame(parent)
        fecha_fallec_frame.grid(row=8, column=1, sticky=tk.W, pady=5)
        self.fecha_fallec = DateEntry(fecha_fallec_frame, width=15, background='darkblue',
                                      foreground='white', date_pattern='dd/mm/yyyy')
        self.fecha_fallec.pack(side=tk.LEFT)
        ttk.Label(fecha_fallec_frame, text=" Hora: ").pack(side=tk.LEFT)
        self.hora_fallec_var = tk.StringVar(value="00")
        self.minuto_fallec_var = tk.StringVar(value="00")
        hora_spin = ttk.Spinbox(fecha_fallec_frame, from_=0, to=23, width=2, textvariable=self.hora_fallec_var, format="%02.0f")
        hora_spin.pack(side=tk.LEFT)
        ttk.Label(fecha_fallec_frame, text=":").pack(side=tk.LEFT)
        minuto_spin = ttk.Spinbox(fecha_fallec_frame, from_=0, to=59, width=2, textvariable=self.minuto_fallec_var, format="%02.0f")
        minuto_spin.pack(side=tk.LEFT)
        
        # Órganos para donar (Checkbuttons)
        ttk.Label(parent, text="Órganos para Donar:").grid(row=9, column=0, sticky=tk.NW, pady=5)
        
        # Frame para contener los checkbuttons de órganos
        organos_frame = ttk.Frame(parent)
        organos_frame.grid(row=9, column=1, sticky=tk.W, pady=5)
        
        # Crear variables y checkbuttons para cada tipo de órgano
        self.organ_vars = {}
        
        # Organizar los checkbuttons en columnas
        organs_per_column = 5
        for i, organo in enumerate([tipo.value for tipo in TipoOrgano]):
            # Calcular posición en la grid
            col = i // organs_per_column
            row = i % organs_per_column
            
            var = tk.BooleanVar(value=False)
            self.organ_vars[organo] = var
            
            # Crear y posicionar el checkbutton
            chk = ttk.Checkbutton(organos_frame, text=organo, variable=var)
            chk.grid(row=row, column=col, sticky=tk.W, padx=(0 if col == 0 else 10))
    
    def update_centro_combo(self):
        # Obtener los centros de salud registrados en INCUCAI
        centros = [centro.nombre for centro in self.incucai.centros_salud]
        self.centro_combo['values'] = centros
        if centros:
            self.centro_combo.current(0)
        else:
            self.centro_var.set('')  # Si no hay centro limpio el combo
    
    def validate_fields(self):
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
        
        # Validar que al menos un órgano esté seleccionado
        if not any(self.organ_vars.values()):
            messagebox.showerror("Error", "Por favor, seleccione al menos un órgano para donar.")
            return False
        
        return True
    
    def register_donante(self):
        if not self.validate_fields():
            return
        
        try:
            # Obtener los datos del formulario
            nombre = self.nombre_var.get().strip()
            dni = int(self.dni_var.get().strip())
            fecha_nacimiento = datetime.strptime(self.fecha_nac.get(), "%d/%m/%Y").date()
            sexo = self.sexo_var.get()
            telefono = int(self.telefono_var.get().strip())
            tipo_sangre = self.sangre_var.get()
            
            # Buscar el centro de salud seleccionado
            centro_nombre = self.centro_var.get()
            centro = None
            for c in self.incucai.centros_salud:
                if c.nombre == centro_nombre:
                    centro = c
                    break
            
            if not centro:
                messagebox.showerror("Error", f"Centro de salud '{centro_nombre}' no encontrado.")
                return
            
            # Crear fecha y hora de fallecimiento
            fecha_str = self.fecha_fallec.get()
            hora = int(self.hora_fallec_var.get())
            minuto = int(self.minuto_fallec_var.get())
            fecha_fallecimiento = datetime.strptime(f"{fecha_str} {hora:02d}:{minuto:02d}", "%d/%m/%Y %H:%M")
            
            # Obtener los órganos seleccionados
            organos_seleccionados = []
            for organo, var in self.organ_vars.items():
                if var.get():
                    organos_seleccionados.append(organo)
            
            # Crear el donante - La clase Donante ya se encarga de convertir los tipos de órganos
            # en objetos Organo dentro de su constructor, según vemos en la definición:
            # self.organos_d = [Organo(tipo,fecha_fallec, incucai) for tipo in organos_d]
            donante = Donante(
                nombre, dni, fecha_nacimiento, sexo, telefono,
                tipo_sangre, centro, self.incucai, fecha_fallecimiento, 
                organos_seleccionados
            )
            
            messagebox.showinfo("Éxito", f"Donante {nombre} registrado exitosamente.")
            self.clear_fields()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar donante: {str(e)}")
    
    def clear_fields(self):
        self.nombre_var.set("")
        self.dni_var.set("")
        self.fecha_nac.set_date(datetime.now().date())
        self.sexo_var.set("femenino")
        self.telefono_var.set("")
        self.sangre_var.set(TipoSangre.A_POSITIVO.value)
        self.centro_var.set("")
        self.fecha_fallec.set_date(datetime.now().date())
        self.hora_fallec_var.set("00")
        self.minuto_fallec_var.set("00")
        
        # Limpiar selección de órganos
        for var in self.organ_vars.values():
            var.set(False)
