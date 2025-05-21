from datetime import datetime

from pacientes.receptor import Receptor
from pacientes.donante import Donante
from pacientes.donante_vivo import DonanteVivo

from cirujanos.cirujano_especial import Cirujano_especial
from cirujanos.cirujano_general import Cirujano_general

from localizables.centro_de_salud import CentroDeSalud
from localizables.vehiculos_terrestres import VehiculoTerrestre
from localizables.helicoptero import Helicoptero
from localizables.avion import Avion

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

class Registros(): 
    # Usar logging ?
    def __init__(self):
        pass

    def Registrar(self,incucai):   

        fecha_nacimiento = datetime.strptime("14/08/2024", "%d/%m/%Y").date()
        fecha=datetime.strptime("14/05/2025", "%d/%m/%Y").date()
        fecha_ingreso = datetime.strptime("11/10/2006 19:00", "%d/%m/%Y %H:%M")
        fecha_ingreso2 = datetime.strptime("10/10/2008 18:00", "%d/%m/%Y %H:%M")
        fecha_fallecimiento = datetime.strptime("17/5/2025 13:30", "%d/%m/%Y %H:%M")

        F = "femenino"
        M = "masculino"
        si = True
        no = False
        


        AZUL = "\033[1;34m"
        RESET = "\033[0m"

        print(f"\n{AZUL}★ SISTEMA DE TRASPLANTES - REGISTROS ★{RESET}")

        # Crear centros de salud
        print(f"\n{AZUL}── Centros de salud ──{RESET}")
        Otamendi = CentroDeSalud("Otamendi", "Callao 3000", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        Favaloro = CentroDeSalud("Favaloro", "Sarmiento 1855", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        ItalianoCordoba = CentroDeSalud("Italiano de Cordoba", "Roma 550", "General paz", "Cordoba", "Argentina", incucai)

        # Crear vehículos
        print(f"\n{AZUL}── Vehículos terrestres ──{RESET}")
        #Ambulancia = VehiculoTerrestre("ambulancia",20, "Corrientes 200", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", Favaloro incucai)
        #Ambulancia2 = VehiculoTerrestre("ambulancia",40, "Corrientes 200", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", Favaloro, incucai)

        print(f"\n{AZUL}── Aviones ──{RESET}")
        #Avion1 = Avion("avion",100, "Callao 2500", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", Favaloro, incucai)
        Avion2 = Avion("avion2",200, "Callao 2500", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", Favaloro, incucai)

        print(f"\n{AZUL}── Helicópteros ──{RESET}")
        #Helicoptero1 = Helicoptero("helicoptero",300, "Roma 550", "General paz", "Cordoba", "Argentina", Favaloro, incucai)

        # Crear donantes
        print(f"\n{AZUL}── Donantes ──{RESET}")
        PersonaInfo = ""# Esto viene de donante_vivo.py crear clase para datos personas asi no pasamos todo en carlos
        Carlos = DonanteVivo("Carlos", 409992, fecha, M, 112324256, TipoSangre.A_POSITIVO.value, Favaloro, incucai, [TipoOrganoVivo.HIGADO.value])

        # Crear receptores
        print(f"\n{AZUL}── Receptores ──{RESET}")
        Zoe = Receptor("Zoe", 46091127,fecha_nacimiento, F, 1158141032, TipoSangre.A_POSITIVO.value, ItalianoCordoba, incucai, "higado", fecha_ingreso, TipoPatologiaHigado.CANCER.value, no)

        # Crear cirujanos
        print(f"\n{AZUL}── Cirujanos generales ──{RESET}")

        print(f"\n{AZUL}── Cirujanos especializados ──{RESET}")
        Juan = Cirujano_especial("Juan", 445, Especialidad.GASTROENTEROLOGO.value, Favaloro, incucai)
        Pepe = Cirujano_especial("Pepe", 334, Especialidad.GASTROENTEROLOGO.value, ItalianoCordoba, incucai)

        print(f"\n{AZUL}═════════════════════════════════════════════════════════════════════{RESET}")




