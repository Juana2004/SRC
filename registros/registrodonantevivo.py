from registros.paparegistro import RegistroBaseApp
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Importaciones de pacientes
from pacientes.donante_vivo import DonanteVivo

# Importaciones de tipos
from tipos.tipo_organos_vivos import TipoOrganoVivo


class RegistroDonanteVivoApp(RegistroBaseApp):
    def __init__(self, root, incucai):
        super().__init__(root, incucai, "Registro de Donantes Vivos")
        
        # Creación de los campos específicos de donante vivo
        self.crear_campos_donante_vivo()
        
        # Agregar botones de acción en la fila 10
        self.agregar_botones(10, self.register_donante_vivo, self.clear_fields)
    
    def crear_campos_donante_vivo(self):
        # Mensaje informativo sobre la ablación
        ttk.Label(self.main_frame, text="Información de Ablación:").grid(row=8, column=0, sticky=tk.W, pady=5)
        info_frame = ttk.Frame(self.main_frame)
        info_frame.grid(row=8, column=1, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text="Los datos de ablación se completarán cuando se programe la cirugía", 
                 font=("Segoe UI", 8), foreground="#666").pack(pady=5)
        
        # Órganos que puede donar (Checkbuttons)
        organos_vivos = [tipo.value for tipo in TipoOrganoVivo]
        self.organ_vars = self.crear_checkbuttons_organos(
            self.main_frame, 9, organos_vivos, "Órganos para Donar:", 3)
    
    def validate_fields(self):
        # Primero validar los campos base
        if not self.validate_fields_base():
            return False
        
        # Validar que al menos un órgano esté seleccionado
        if not any(self.organ_vars.values()):
            messagebox.showerror("Error", "Por favor, seleccione al menos un órgano para donar.")
            return False
        
        return True
    
    def register_donante_vivo(self):
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
            
            # Obtener los órganos seleccionados
            organos_seleccionados = []
            for organo, var in self.organ_vars.items():
                if var.get():
                    organos_seleccionados.append(organo)
            
            # Crear el donante vivo
            donante_vivo = DonanteVivo(
                nombre, dni, fecha_nacimiento, sexo, telefono,
                tipo_sangre, centro, self.incucai, organos_seleccionados
            )
            
            messagebox.showinfo("Éxito", f"Donante vivo {nombre} registrado exitosamente.\n\nLos datos de ablación se completarán cuando se programe la cirugía.")
            self.clear_fields()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar donante vivo: {str(e)}")
    
    def clear_fields(self):
        # Limpiar campos base
        self.clear_fields_base()
        
        # Limpiar selección de órganos
        for var in self.organ_vars.values():
            var.set(False)