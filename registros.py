from datetime import datetime
from incucai import INCUCAI

#import tkinter as tk
#from tkinter import ttk, messagebox

from pacientes.receptor import Receptor
from pacientes.donante import Donante
from pacientes.donante_vivo import DonanteVivo

from cirujanos.cirujano_especial import Cirujano_especial

from localizables.centro_de_salud import CentroDeSalud
from localizables.vehiculos_terrestres import VehiculoTerrestre
from localizables.helicoptero import Helicoptero
from localizables.avion import Avion

from organos.organo import Organo
from organos.organoo import Organoo

from tipos.tipo_especialidad import Especialidad
from tipos.tipo_organo import TipoOrgano
from tipos.tipo_organos_vivos import TipoOrganoVivo
from tipos.tipo_sangre import TipoSangre
from tipos.tipo_patologia_corazon import TipoPatologiaCorazon
from tipos.tipo_patologia_higado import TipoPatologiaHigado




class Registros():
    def __init__(self):
        pass

    def Registrar(self):   
        incucai = INCUCAI()


        fecha_nacimiento = datetime.strptime("14/8/2004", "%d/%m/%Y").date()
        fecha_ingreso = datetime.strptime("11/10/2006 19:00", "%d/%m/%Y %H:%M")
        fecha_ingreso2 = datetime.strptime("10/10/2008 18:00", "%d/%m/%Y %H:%M")
        fecha_fallecimiento = datetime.strptime("17/5/2025 13:30", "%d/%m/%Y %H:%M")

        F = "femenino"
        M = "masculino"
        si = True
        no = False
        


        print("\n-------------Registros------------")
        # Crear centros de salud
        Otamendi = CentroDeSalud("Otamendi", "Callao 3000", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        Favaloro = CentroDeSalud("Favaloro", "Sarmiento 1855", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        #ItalianoCordoba = CentroDeSalud("Italiano de Cordoba", "Roma 550", "General paz", "Cordoba", "Argentina", incucai)

        # Crear vehiculos
        Ambulancia = VehiculoTerrestre("ambulancia",20, "Corrientes 200", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        #Ambulancia2 = VehiculoTerrestre(40, "Corrientes 200", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        #Avion1 = Avion(100, "Callao 2500", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        #Helicoptero1 = Helicoptero(300, "Roma 550", "General paz", "Cordoba", "Argentina", incucai)

        #crear organo
        Higado1=Organo(TipoOrgano.HIGADO.value, fecha_fallecimiento, incucai)
        Higado2=Organo(TipoOrgano.HIGADO.value, fecha_fallecimiento, incucai)
        Corazon1=Organo(TipoOrgano.CORAZON.value, fecha_fallecimiento, incucai)
        Corazon2=Organo(TipoOrgano.CORAZON.value, fecha_fallecimiento, incucai)
        Higado3=Organoo(TipoOrganoVivo.HIGADO.value, incucai)
        

        #crear receptores
        Juana = Receptor("Juana", 46091128, fecha_nacimiento, F, 1158141032, TipoSangre.A_POSITIVO.value, Otamendi,incucai, TipoOrgano.CORAZON.value, fecha_ingreso, TipoPatologiaCorazon.INSUFICIENCIA_C.value,si )
        Zoe = Receptor("Zoe", 46091127, fecha_nacimiento, F, 1158141032, TipoSangre.A_POSITIVO.value, Otamendi, incucai, TipoOrgano.HIGADO.value, fecha_ingreso2, TipoPatologiaHigado.HEPATITIS.value,si )

        #crear donantes
        Cami = Donante("Cami", 4600914, fecha_nacimiento, F, 1158143232, TipoSangre.A_POSITIVO.value, Favaloro, incucai, fecha_fallecimiento, [Higado1, Corazon2])
        Tere = Donante("Tere", 4600912, fecha_nacimiento, F, 1158143232, TipoSangre.A_POSITIVO.value, Favaloro, incucai, fecha_fallecimiento, [Higado2, Corazon1])
        Carlos = DonanteVivo("Carlos", 409992, fecha_nacimiento, M, 112324256, TipoSangre.A_POSITIVO.value, Favaloro, incucai, [Higado3])
        
        #crear cirujanos
        Juan = Cirujano_especial("Juan", 445, Especialidad.GASTROENTEROLOGO.value, Otamendi, incucai)
        #Carlos = Cirujano_especial("Carlos", 334, Especialidad.GASTROENTEROLOGO.value, ItalianoCordoba, incucai)
        """
        try:
            nombre = entry_nombre.get()
            dni = int(entry_dni.get())
            fecha_nac = datetime.strptime(entry_nac.get(), "%d/%m/%Y").date()
            sexo = combo_sexo.get()
            telefono = int(entry_tel.get())
            tipo_sangre = getattr(TipoSangre, combo_sangre.get()).value
            tipo_organo = getattr(TipoOrgano, combo_organo.get()).value
            fecha_ing = datetime.strptime(entry_ingreso.get(), "%d/%m/%Y %H:%M")
            urgente = combo_urgente.get() == "Sí"

            # Patología según órgano
            if combo_organo.get() == "CORAZON":
                patologia = getattr(TipoPatologiaCorazon, combo_patologia.get())
            else:
                patologia = getattr(TipoPatologiaHigado, combo_patologia.get())

            Receptor(nombre, dni, fecha_nac, sexo, telefono, tipo_sangre,
                    Otamendi, incucai, tipo_organo, fecha_ing, patologia, urgente)

            messagebox.showinfo("Éxito", f"Receptor {nombre} registrado con éxito.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

        # GUI con Tkinter
        root = tk.Tk()
        root.title("Registro de Receptor - INCUCAI")

        # Campos
        tk.Label(root, text="Nombre:").grid(row=0, column=0)
        entry_nombre = tk.Entry(root)
        entry_nombre.grid(row=0, column=1)

        tk.Label(root, text="DNI:").grid(row=1, column=0)
        entry_dni = tk.Entry(root)
        entry_dni.grid(row=1, column=1)

        tk.Label(root, text="Fecha Nacimiento (dd/mm/yyyy):").grid(row=2, column=0)
        entry_nac = tk.Entry(root)
        entry_nac.grid(row=2, column=1)

        tk.Label(root, text="Sexo:").grid(row=3, column=0)
        combo_sexo = ttk.Combobox(root, values=["femenino", "masculino"])
        combo_sexo.grid(row=3, column=1)

        tk.Label(root, text="Teléfono:").grid(row=4, column=0)
        entry_tel = tk.Entry(root)
        entry_tel.grid(row=4, column=1)

        tk.Label(root, text="Tipo de Sangre:").grid(row=5, column=0)
        combo_sangre = ttk.Combobox(root, values=[ts.name for ts in TipoSangre])
        combo_sangre.grid(row=5, column=1)

        tk.Label(root, text="Órgano que necesita:").grid(row=6, column=0)
        combo_organo = ttk.Combobox(root, values=[to.name for to in TipoOrgano])
        combo_organo.grid(row=6, column=1)

        tk.Label(root, text="Fecha de ingreso (dd/mm/yyyy HH:MM):").grid(row=7, column=0)
        entry_ingreso = tk.Entry(root)
        entry_ingreso.grid(row=7, column=1)

        tk.Label(root, text="Patología:").grid(row=8, column=0)
        combo_patologia = ttk.Combobox(root)
        combo_patologia.grid(row=8, column=1)

        tk.Label(root, text="¿Es urgente?").grid(row=9, column=0)
        combo_urgente = ttk.Combobox(root, values=["Sí", "No"])
        combo_urgente.grid(row=9, column=1)

        # Botón de registrar
        tk.Button(root, text="Registrar", command=incucai.registrar_receptor).grid(row=10, column=0, columnspan=2, pady=10)

        # Cambiar opciones de patología dinámicamente
        def actualizar_patologias(event):
            if combo_organo.get() == "CORAZON":
                combo_patologia["values"] = [p.name for p in TipoPatologiaCorazon]
            elif combo_organo.get() == "HIGADO":
                combo_patologia["values"] = [p.name for p in TipoPatologiaHigado]
            else:
                combo_patologia["values"] = []

        combo_organo.bind("<<ComboboxSelected>>", actualizar_patologias)

        # Iniciar GUI
        root.mainloop()
        """
        print("\n-----------------------------------------")

        incucai.mostrar_lista_espera()
        incucai.match()
        incucai.mostrar_estado()
