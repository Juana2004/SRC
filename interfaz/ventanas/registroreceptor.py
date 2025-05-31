from .registro_pacientes import RegistroBaseApp
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from pacientes.receptor import Receptor

from tipos.tipo_organo import TipoOrgano
from tipos.patologias import *

from clases_type.datos_personales import DatosPersonales

from excepciones import ErrorDNIRepetido


class RegistroReceptorApp(RegistroBaseApp):
    def __init__(self, root, incucai):
        super().__init__(root, incucai, "Registro de Receptor")
        
        self.crear_campos_receptor()
        
        self.agregar_botones(12, self.register_receptor, self.clear_fields)
    
    def crear_campos_receptor(self):
        ttk.Label(self.main_frame, text="Órgano que necesita:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.organo_var = tk.StringVar()
        organo_combo = ttk.Combobox(self.main_frame, textvariable=self.organo_var, width=27)
        organo_combo['values'] = [tipo.value for tipo in TipoOrgano]
        organo_combo.grid(row=8, column=1, sticky=tk.W, pady=5)
        organo_combo.current(0)
        organo_combo.bind("<<ComboboxSelected>>", self.update_patologia_options)
        
        self.fecha_ingreso, self.hora_var, self.minuto_var = self.crear_frame_fecha_hora(
            self.main_frame, "Fecha de Ingreso:", 9)

        ttk.Label(self.main_frame, text="Patología:").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.patologia_var = tk.StringVar()
        self.patologia_combo = ttk.Combobox(self.main_frame, textvariable=self.patologia_var, width=27)
        self.update_patologia_options(None)  
        self.patologia_combo.grid(row=10, column=1, sticky=tk.W, pady=5)
 
        ttk.Label(self.main_frame, text="Urgencia:").grid(row=11, column=0, sticky=tk.W, pady=5)
        self.urgencia_var = tk.StringVar()
        urgencia_combo = ttk.Combobox(self.main_frame, textvariable=self.urgencia_var, width=27)
        urgencia_combo['values'] = ['si', 'no']
        urgencia_combo.grid(row=11, column=1, sticky=tk.W, pady=5)
        urgencia_combo.current(1)
    
    def get_tipo_patologia_por_organo(self, organo):
        patologias_por_organo = {
            TipoOrgano.CORAZON.value: TipoPatologiaCorazon,
            TipoOrgano.CORNEAS.value: TipoPatologiaCorneas,
            TipoOrgano.HIGADO.value: TipoPatologiaHigado,
            TipoOrgano.PIEL.value: TipoPatologiaPiel,
            TipoOrgano.RINION.value: TipoPatologiaRinion,
            TipoOrgano.PANCREAS.value: TipoPatologiaPancreas,
            TipoOrgano.HUESOS.value: TipoPatologiaHuesos,
            TipoOrgano.PULMON.value: TipoPatologiaPulmon,
            TipoOrgano.INTESTINO.value: TipoPatologiaIntestino
        }
        
        if organo in patologias_por_organo:
            return list(patologias_por_organo[organo])
        else:
            return []
    
    def update_patologia_options(self, event):
        organo = self.organo_var.get()
        tipo_patologia = self.get_tipo_patologia_por_organo(organo)
        
        nombres_patologias = [p.name for p in tipo_patologia]
        
        self.patologia_combo['values'] = nombres_patologias
        if nombres_patologias:
            self.patologia_var.set(nombres_patologias[0])
    
    def validate_fields(self):
        if not self.validar_campos():
            return False
        
        if not self.patologia_var.get():
            messagebox.showerror("Error", "Por favor, seleccione una patología.")
            return False
        
        return True
    
    def register_receptor(self):
        if not self.validate_fields():
            return
        
        try:
            nombre = self.nombre_var.get().strip()
            dni = int(self.dni_var.get().strip())
            fecha_nacimiento = datetime.strptime(self.fecha_nac.get(), "%d/%m/%Y").date()
            sexo = self.sexo_var.get()
            telefono = int(self.telefono_var.get().strip())
            tipo_sangre = self.sangre_var.get()
            
            centro = self.obtener_centro_salud()
            if not centro:
                messagebox.showerror("Error", f"Centro de salud '{self.centro_var.get()}' no encontrado.")
                return
            
            organo = self.organo_var.get()

            nombre_patologia = self.patologia_var.get()

            tipo_patologia = self.get_tipo_patologia_por_organo(organo)
            patologia_obj = None
            for p in tipo_patologia:
                if p.name == nombre_patologia:
                    patologia_obj = p
                    break

            fecha_ingreso = self.widgets_hora(
                self.fecha_ingreso, self.hora_var, self.minuto_var)
            
            urgencia = self.urgencia_var.get() == "si"
            
            if patologia_obj is None:
                messagebox.showerror("Error", f"Patología '{nombre_patologia}' no encontrada para el órgano {organo}.")
                return

            datos = DatosPersonales(nombre, dni, fecha_nacimiento, sexo, telefono)

            receptor = Receptor(
                datos, tipo_sangre, centro,
                organo, fecha_ingreso, patologia_obj.value, urgencia
            )

            messagebox.showinfo("Éxito", f"Receptor {nombre} registrado exitosamente.")
            self.clear_fields()
        
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar receptor: {str(e)}")
    
    def clear_fields(self):
        self.clear_fields_base()
        self.organo_var.set(TipoOrgano.CORAZON.value)
        self.fecha_ingreso.set_date(datetime.now().date())
        self.hora_var.set("00")
        self.minuto_var.set("00")
        self.update_patologia_options(None)
        self.urgencia_var.set("no")