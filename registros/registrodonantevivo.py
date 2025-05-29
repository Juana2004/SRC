from registros.registrointerfaz import RegistroBaseApp
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from tipos.tipo_organos_vivos import TipoOrganoVivo
from organos.organo_vivo import OrganoVivo
from pacientes.donante_vivo import DonanteVivo
from clases_type.datos_personales import DatosPersonales

class RegistroDonanteVivoApp(RegistroBaseApp):
    def __init__(self, root, incucai):
        super().__init__(root, incucai, "Registro de Donante Vivo")
        self.crear_campos_donante_vivo()
        self.agregar_botones(11, self.registrar_donante_vivo, self.clear_fields)

    def crear_campos_donante_vivo(self):
        ttk.Label(self.main_frame, text="Órganos a donar:").grid(row=8, column=0, sticky=tk.W, pady=5)

        organo_frame = ttk.Frame(self.main_frame)
        organo_frame.grid(row=8, column=1, columnspan=2, sticky="nsew", padx=5)

        self.organo_vars = {}
        for i, tipo in enumerate(TipoOrganoVivo):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(organo_frame, text=tipo.value, variable=var)
            chk.grid(row=i // 2, column=i % 2, sticky=tk.W, padx=10, pady=2)
            self.organo_vars[tipo] = var

        organo_frame.columnconfigure(0, weight=1)
        organo_frame.columnconfigure(1, weight=1)

    def validate_fields(self):
        if not self.validate_fields_base():
            return False
        if not any(var.get() for var in self.organo_vars.values()):
            messagebox.showerror("Error", "Debe seleccionar al menos un órgano para donar.")
            return False
        return True

    def registrar_donante_vivo(self):
        if not self.validate_fields():
            return

        try:
            nombre = self.nombre_var.get().strip()
            dni = int(self.dni_var.get().strip())
            fecha_nacimiento = datetime.strptime(self.fecha_nac.get(), "%d/%m/%Y").date()
            sexo = self.sexo_var.get()
            telefono = int(self.telefono_var.get().strip())
            tipo_sangre = self.sangre_var.get()

            centro = self.get_centro_salud()
            if not centro:
                messagebox.showerror("Error", f"Centro de salud '{self.centro_var.get()}' no encontrado.")
                return


            organos_tipo = [tipo.value for tipo, var in self.organo_vars.items() if var.get()]
            if not organos_tipo:
                messagebox.showerror("Error", "Debe seleccionar al menos un órgano para donar.")
                return

            datos = DatosPersonales(nombre, dni, fecha_nacimiento, sexo, telefono)
            donante = DonanteVivo(datos, tipo_sangre, centro, organos_tipo)

            messagebox.showinfo("Éxito", f"Donante vivo {nombre} registrado exitosamente.")
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar donante vivo: {str(e)}")

    def clear_fields(self):
        self.clear_fields_base()
        for var in self.organo_vars.values():
            var.set(False)
     