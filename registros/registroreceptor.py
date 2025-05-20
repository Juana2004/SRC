from registros.paparegistro import RegistroBaseApp
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Importaciones de pacientes
from pacientes.receptor import Receptor

# Importaciones de tipos
from tipos.tipo_organo import TipoOrgano
from tipos.tipo_patologia_corazon import TipoPatologiaCorazon
from tipos.tipo_patologia_higado import TipoPatologiaHigado
from tipos.tipo_patologia_corneas import TipoPatologiaCorneas
from tipos.tipo_patologia_piel import Tipo_Patologia_Piel
from tipos.tipo_patologia_rinion import TipoPatologiaRinion
from tipos.tipo_patologia_pancreas import TipoPatologiaPancreas
from tipos.tipo_patologia_huesos import TipoPatologiaHuesos
from tipos.tipo_patologia_pulmon import TipoPatologiaPulmon
from tipos.tipo_patologia_intestino import TipoPatologiaIntestino


class RegistroReceptorApp(RegistroBaseApp):
    def __init__(self, root, incucai):
        super().__init__(root, incucai, "Registro de Receptor")
        
        # Creación de los campos específicos de receptor
        self.crear_campos_receptor()
        
        # Agregar botones de acción en la fila 12
        self.agregar_botones(12, self.register_receptor, self.clear_fields)
    
    def crear_campos_receptor(self):
        # Órgano que necesita
        ttk.Label(self.main_frame, text="Órgano que necesita:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.organo_var = tk.StringVar()
        organo_combo = ttk.Combobox(self.main_frame, textvariable=self.organo_var, width=27)
        organo_combo['values'] = [tipo.value for tipo in TipoOrgano]
        organo_combo.grid(row=8, column=1, sticky=tk.W, pady=5)
        organo_combo.current(0)
        organo_combo.bind("<<ComboboxSelected>>", self.update_patologia_options)
        
        # Fecha de ingreso
        self.fecha_ingreso, self.hora_var, self.minuto_var = self.crear_frame_fecha_hora(
            self.main_frame, "Fecha de Ingreso:", 9)
        
        # Patología
        ttk.Label(self.main_frame, text="Patología:").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.patologia_var = tk.StringVar()
        self.patologia_combo = ttk.Combobox(self.main_frame, textvariable=self.patologia_var, width=27)
        self.update_patologia_options(None)  # Inicializar opciones
        self.patologia_combo.grid(row=10, column=1, sticky=tk.W, pady=5)
        
        # Urgencia
        ttk.Label(self.main_frame, text="Urgencia:").grid(row=11, column=0, sticky=tk.W, pady=5)
        self.urgencia_var = tk.StringVar()
        urgencia_combo = ttk.Combobox(self.main_frame, textvariable=self.urgencia_var, width=27)
        urgencia_combo['values'] = ['si', 'no']
        urgencia_combo.grid(row=11, column=1, sticky=tk.W, pady=5)
        urgencia_combo.current(1)
    
    def get_tipo_patologia_por_organo(self, organo):
        # Retorna el Enum de patologías correspondiente al órgano seleccionado.
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
        # Primero validar los campos base
        if not self.validate_fields_base():
            return False
        
        # Validar que haya una patología seleccionada
        if not self.patologia_var.get():
            messagebox.showerror("Error", "Por favor, seleccione una patología.")
            return False
        
        return True
    
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
            
            # Obtener el centro de salud
            centro = self.get_centro_salud()
            if not centro:
                messagebox.showerror("Error", f"Centro de salud '{self.centro_var.get()}' no encontrado.")
                return
            
            # Obtener el órgano
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
            fecha_ingreso = self.get_datetime_from_widgets(
                self.fecha_ingreso, self.hora_var, self.minuto_var)
            
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
        # Limpiar campos base
        self.clear_fields_base()
        
        # Limpiar campos específicos
        self.organo_var.set(TipoOrgano.CORAZON.value)
        self.fecha_ingreso.set_date(datetime.now().date())
        self.hora_var.set("00")
        self.minuto_var.set("00")
        self.update_patologia_options(None)
        self.urgencia_var.set("no")