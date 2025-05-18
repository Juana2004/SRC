from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from pacientes.receptor import Receptor
from pacientes.donante import Donante
from pacientes.donante_vivo import DonanteVivo

from tipos.tipo_especialidad import Especialidad
from tipos.tipo_organo import TipoOrgano
from tipos.tipo_organos_vivos import TipoOrganoVivo
from tipos.tipo_sangre import TipoSangre
from tipos.tipo_patologia_corazon import TipoPatologiaCorazon
from tipos.tipo_patologia_higado import TipoPatologiaHigado
from tipos.tipo_patologia_corneas import TipoPatologiaCorneas
from tipos.tipo_patologia_piel import Tipo_Patologia_Piel
from tipos.tipo_patologia_rinion import TipoPatologiaRinion
from tipos.tipo_patologia_pancreas import TipoPatologiaPancreas
from tipos.tipo_patologia_huesos import TipoPatologiaHuesos 
from tipos.tipo_patologia_pulmon import TipoPatologiaPulmon
from tipos.tipo_patologia_intestino import TipoPatologiaIntestino

#registrar receptores con interfaz 

class RegistroReceptorApp():
    def __init__(self, root, incucai):
        self.root = root
        self.incucai = incucai
        self.root.title("Registro de Receptores")
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
        ttk.Label(main_frame, text="Registro de Receptores", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="n")

        # Creación de los campos
        self.create_fields(main_frame)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=12, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Registrar", command=self.register_receptor, style="Accent.TButton").grid(row=0, column=0, padx=10)
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
        
        # Órgano que necesita
        ttk.Label(parent, text="Órgano que necesita:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.organo_var = tk.StringVar()
        organo_combo = ttk.Combobox(parent, textvariable=self.organo_var, width=27)
        organo_combo['values'] = [tipo.value for tipo in TipoOrgano]
        organo_combo.grid(row=8, column=1, sticky=tk.W, pady=5)
        organo_combo.current(0)
        organo_combo.bind("<<ComboboxSelected>>", self.update_patologia_options)
        
        # Fecha de ingreso
        ttk.Label(parent, text="Fecha de Ingreso:").grid(row=9, column=0, sticky=tk.W, pady=5)
        fecha_ingreso_frame = ttk.Frame(parent)
        fecha_ingreso_frame.grid(row=9, column=1, sticky=tk.W, pady=5)
        
        self.fecha_ingreso = DateEntry(fecha_ingreso_frame, width=15, background='darkblue', 
                                       foreground='white', date_pattern='dd/mm/yyyy')
        self.fecha_ingreso.pack(side=tk.LEFT)
        
        ttk.Label(fecha_ingreso_frame, text=" Hora: ").pack(side=tk.LEFT)
        
        self.hora_var = tk.StringVar(value="00")
        self.minuto_var = tk.StringVar(value="00")
        
        hora_spin = ttk.Spinbox(fecha_ingreso_frame, from_=0, to=23, width=2, textvariable=self.hora_var, format="%02.0f")
        hora_spin.pack(side=tk.LEFT)
        
        ttk.Label(fecha_ingreso_frame, text=":").pack(side=tk.LEFT)
        
        minuto_spin = ttk.Spinbox(fecha_ingreso_frame, from_=0, to=59, width=2, textvariable=self.minuto_var, format="%02.0f")
        minuto_spin.pack(side=tk.LEFT)
        
        #patologia
        ttk.Label(parent, text="Patología:").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.patologia_var = tk.StringVar()
        self.patologia_combo = ttk.Combobox(parent, textvariable=self.patologia_var, width=27)
        self.update_patologia_options(None)  # Inicializar opciones
        self.patologia_combo.grid(row=10, column=1, sticky=tk.W, pady=5)
        
        # Urgencia
        ttk.Label(parent, text="Urgencia:").grid(row=11, column=0, sticky=tk.W, pady=5)
        self.urgencia_var = tk.StringVar()
        urgencia_combo = ttk.Combobox(parent, textvariable=self.urgencia_var, width=27)
        urgencia_combo['values'] = ['si', 'no']
        urgencia_combo.grid(row=11, column=1, sticky=tk.W, pady=5)
        urgencia_combo.current(1)
    
    def update_centro_combo(self):
        # Obtener los centros de salud registrados en INCUCAI
        centros = [centro.nombre for centro in self.incucai.centros_salud]
        self.centro_combo['values'] = centros
        if centros:
            self.centro_combo.current(0)
        else:
            self.centro_var.set('') #si no hay centro limpio el combo

    def get_tipo_patologia_por_organo(self, organo):
   
    #Retorna el Enum de patologías correspondiente al órgano seleccionado.
    
    # Mapeo de órganos a sus patologías correspondientes
        patologias_por_organo = {
            TipoOrgano.CORAZON.value: TipoPatologiaCorazon,
            TipoOrgano.CORNEAS.value: TipoPatologiaCorneas,
            TipoOrgano.HIGADO.value: TipoPatologiaHigado,
            TipoOrgano.PIEL.value: Tipo_Patologia_Piel,
            TipoOrgano.RINION.value: TipoPatologiaRinion,
            TipoOrgano.PANCREAS.value: TipoPatologiaPancreas,
            TipoOrgano.HUESOS.value: TipoPatologiaHuesos,
            TipoOrgano.PULMON.value: TipoPatologiaPulmon,
            TipoOrgano.INTESTINO.value: TipoPatologiaIntestino
        }
    
        # Obtener el enum de patologías correspondiente
        if organo in patologias_por_organo:
            return list(patologias_por_organo[organo])
        else:
            # Si no hay patologías definidas para este órgano, retornar una lista vacía
            return []
        
    def update_patologia_options(self, event):
            organo = self.organo_var.get()
            tipo_patologia = self.get_tipo_patologia_por_organo(organo)
            
            # Obtener los nombres de las patologías
            nombres_patologias = [p.name for p in tipo_patologia]
            
            # Actualizar el combobox con los nombres
            self.patologia_combo['values'] = nombres_patologias
            if nombres_patologias:
                self.patologia_var.set(nombres_patologias[0])
                
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
        
        # Validar que haya una patología seleccionada
        if not self.patologia_var.get():
            messagebox.showerror("Error", "Por favor, seleccione una patología.")
            return False
        
        return True
    
    def get_patologia_nombres(tipo_patologia_enum):
        return [p.name for p in tipo_patologia_enum]
    
    def register_receptor(self):
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
            
            # Obtener el órgano (esta línea debe estar antes de procesar la patología)
            organo = self.organo_var.get()
            
            # Obtener el nombre de la patología seleccionada
            nombre_patologia = self.patologia_var.get()
            
            # Convertir nombre a objeto enum
            tipo_patologia = self.get_tipo_patologia_por_organo(organo)
            patologia_obj = None
            for p in tipo_patologia:
                if p.name == nombre_patologia:
                    patologia_obj = p
                    break
            
            # Crear fecha y hora de ingreso
            fecha_str = self.fecha_ingreso.get()
            hora = int(self.hora_var.get())
            minuto = int(self.minuto_var.get())
            fecha_ingreso = datetime.strptime(f"{fecha_str} {hora:02d}:{minuto:02d}", "%d/%m/%Y %H:%M")
            
            urgencia = self.urgencia_var.get() == "si"
            
            if patologia_obj is None:
                messagebox.showerror("Error", f"Patología '{nombre_patologia}' no encontrada para el órgano {organo}.")
                return
            
            # Crear el receptor con patologia_obj en lugar de patologia
            receptor = Receptor(
                nombre, dni, fecha_nacimiento, sexo, telefono,
                tipo_sangre, centro, self.incucai, organo,
                fecha_ingreso, patologia_obj.value, urgencia
            )
            
            messagebox.showinfo("Éxito", f"Receptor {nombre} registrado exitosamente.")
            self.clear_fields()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar receptor: {str(e)}")
    
    def clear_fields(self):
        self.nombre_var.set("")
        self.dni_var.set("")
        self.fecha_nac.set_date(datetime.now().date())
        self.sexo_var.set("femenino")
        self.telefono_var.set("")
        self.sangre_var.set(TipoSangre.A_POSITIVO.value)
        self.centro_var.set("")
        self.organo_var.set(TipoOrgano.CORAZON.value)
        self.fecha_ingreso.set_date(datetime.now().date())
        self.hora_var.set("00")
        self.minuto_var.set("00")
        self.update_patologia_options(None)
        self.urgencia_var.set("no")
