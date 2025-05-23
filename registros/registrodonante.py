'''from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
# Importamos la clase base para heredar de ella
from registros.paparegistro import RegistroBaseApp
# Importaciones de pacientes
from pacientes.donante import Donante
# Importaciones de tipos
from tipos.tipo_organo import TipoOrgano


class RegistroDonantesApp(RegistroBaseApp):
    """
    Clase para el registro de donantes en el sistema INCUCAI.
    Hereda de RegistroBaseApp para mantener la consistencia con los otros registros.
    """
    def __init__(self, root, incucai):
        super().__init__(root, incucai, titulo="Registro de Donante", tamano="700x650")
        
        # Campos específicos para donantes
        self.crear_campos_donante()
        
        # Agregamos los botones de acción
        self.agregar_botones(11, self.registrar_donante, self.limpiar_campos)
    
    def crear_campos_donante(self):
        """Crea los campos específicos para el registro de donantes"""
        # Fecha y hora de fallecimiento
        self.fecha_fallec, self.hora_fallec_var, self.min_fallec_var = self.crear_frame_fecha_hora(
            self.main_frame, "Fecha/Hora de Fallecimiento:", 8
        )
        
        # No solicitamos fecha de ablación ya que se maneja automáticamente en la clase Donante
        
        # Checkboxes para seleccionar los órganos a donar
        self.organos_vars = self.crear_checkbuttons_organos(
            self.main_frame, 9, [tipo.value for tipo in TipoOrgano], 
            titulo="Órganos para Donar:", organs_per_column=4
        )
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        # Limpiamos los campos base
        self.clear_fields_base()
        
        # Limpiamos los campos específicos de donante
        self.fecha_fallec.set_date(datetime.now().date())
        self.hora_fallec_var.set("00")
        self.min_fallec_var.set("00")
        
        # Desmarcamos todas las casillas de órganos
        for var in self.organos_vars.values():
            var.set(False)
    
    def registrar_donante(self):
        """Registra un nuevo donante en el sistema"""
        # Validamos los campos base primero
        if not self.validate_fields_base():
            return
        
        # Validamos campos específicos de donante
        if not self.validar_campos_donante():
            return
        
        try:
            # Obtenemos el centro de salud
            centro = self.get_centro_salud()
            if not centro:
                messagebox.showerror("Error", "Centro de salud no encontrado.")
                return
            
            # Obtenemos la lista de órganos seleccionados
            organos_seleccionados = []
            for organo, var in self.organos_vars.items():
                if var.get():
                    # Convertimos el valor a enum TipoOrgano
                    for tipo in TipoOrgano:
                        if tipo.value == organo:
                            organos_seleccionados.append(tipo)
                            break
            
            # Verificamos que haya al menos un órgano seleccionado
            if not organos_seleccionados:
                messagebox.showerror("Error", "Debe seleccionar al menos un órgano para donar.")
                return
            
            # Creamos la fecha de fallecimiento
            fecha_fallecimiento = self.get_datetime_from_widgets(
                self.fecha_fallec, self.hora_fallec_var, self.min_fallec_var
            )
            
            # Creamos un nuevo donante
            donante = Donante(
                nombre=self.nombre_var.get().strip(),
                dni=int(self.dni_var.get().strip()),
                fecha_nac=self.fecha_nac.get_date(),
                sexo=self.sexo_var.get(),
                tel=int(self.telefono_var.get().strip()),
                t_sangre=self.sangre_var.get(),
                centro=centro,
                incucai=self.incucai,
                fecha_fallec=fecha_fallecimiento,
                organos_d=organos_seleccionados
            )
            
            # Mostramos mensaje de éxito
            messagebox.showinfo("Éxito", f"Donante {donante.nombre} registrado correctamente.")
            
            # Limpiamos los campos para un nuevo registro
            self.limpiar_campos()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el donante: {str(e)}")
    
    def validar_campos_donante(self):
        """Valida los campos específicos del donante
        
        Returns:
            bool: True si todos los campos son válidos, False en caso contrario
        """
        # Validar que la fecha de nacimiento sea anterior a la fecha actual
        fecha_nac = self.fecha_nac.get_date()
        if fecha_nac >= datetime.now().date():
            messagebox.showerror("Error", "La fecha de nacimiento debe ser anterior a la fecha actual.")
            return False
        
        # Validar fecha y hora de fallecimiento
        try:
            fecha_fallec = self.get_datetime_from_widgets(
                self.fecha_fallec, self.hora_fallec_var, self.min_fallec_var
            )
            
            # Validar que la fecha de fallecimiento sea posterior a la fecha de nacimiento
            if fecha_fallec.date() <= fecha_nac:
                messagebox.showerror("Error", "La fecha de fallecimiento debe ser posterior a la fecha de nacimiento.")
                return False
            
            # Validar que la fecha de fallecimiento no sea futura
            if fecha_fallec > datetime.now():
                messagebox.showerror("Error", "La fecha de fallecimiento no puede ser futura.")
                return False
        except Exception:
            messagebox.showerror("Error", "Fecha u hora de fallecimiento inválida.")
            return False
        
        return True'''