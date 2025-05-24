from datetime import datetime

from pacientes.receptor import Receptor
from pacientes.donante import Donante
from pacientes.donante_vivo import DonanteVivo

from cirujanos.cirujano_especializado import CirujanoEspecializado
from cirujanos.cirujano_general import CirujanoGeneral

from localizables.centro_de_salud import CentroDeSalud
from localizables.vehiculos_terrestres import VehiculoTerrestre
from localizables.helicoptero import Helicoptero
from localizables.avion import Avion

from tipos.tipo_especialidad import Especialidad
from tipos.tipo_organo import TipoOrgano
from tipos.tipo_organos_vivos import TipoOrganoVivo
from tipos.tipo_sangre import TipoSangre
from tipos.patologias import *


class Registros:
    def __init__(self):
        pass

    def Registrar(self, incucai):

        F = "femenino"
        M = "masculino"
        si = True
        no = False

        AZUL = "\033[1;34m"
        RESET = "\033[0m"

        print(f"\n{AZUL}★ SISTEMA DE TRASPLANTES - REGISTROS ★{RESET}")

        '''Crear centros de salud'''
        print(f"\n{AZUL}── Centros de salud ──{RESET}")
        Otamendi = CentroDeSalud(
            "Otamendi",
            "Callao 3000",
            "Ciudad Autonoma de Buenos Aires",
            "Buenos Aires",
            "Argentina",
            incucai,
        )
        Favaloro = CentroDeSalud(
            "Favaloro",
            "Sarmiento 1855",
            "Ciudad Autonoma de Buenos Aires",
            "Buenos Aires",
            "Argentina",
            incucai,
        )
        ItalianoCordoba = CentroDeSalud(
            "Italiano de Cordoba",
            "Roma 550",
            "General paz",
            "Cordoba",
            "Argentina",
            incucai,
        )

        ''' Crear vehículos'''
        print(f"\n{AZUL}── Vehículos terrestres ──{RESET}")
        Ambulancia2 = VehiculoTerrestre(
            "Ambulancia",
            40,
            "Corrientes 200",
            "Ciudad Autonoma de Buenos Aires",
            "Buenos Aires",
            "Argentina",
            Otamendi,
            incucai,
        )

        print(f"\n{AZUL}── Aviones ──{RESET}")

        Avion1 = Avion(
            "avion",
            700,
            "Chacabuco 2000",
            "Carlos Paz",
            "Cordoba", 
            "Argentina", 
            Favaloro, 
            incucai)

        print(f"\n{AZUL}── Helicópteros ──{RESET}")

        Helicoptero1 = Helicoptero(
            "helicoptero",
            300,
            "Roma 550",
            "General paz",
            "Cordoba",
            "Argentina",
            Favaloro,
            incucai,
        )

        print(f"\n{AZUL}── Donantes ──{RESET}")
       
        fecha_nacimiento_carlos = datetime.strptime("14/05/2002", "%d/%m/%Y").date()
        Carlos = DonanteVivo(
            "Carlos",
            409992,
            fecha_nacimiento_carlos,
            M,
            112324256,
            TipoSangre.O_NEGATIVO.value,
            Favaloro,
            incucai,
            [TipoOrganoVivo.HIGADO.value, TipoOrganoVivo.INTESTINO.value],
        )

        fecha_fallecimiento_tere = datetime.strptime("17/5/2025 13:30", "%d/%m/%Y %H:%M")
        fecha_nacimiento_tere = datetime.strptime("17/5/2003", "%d/%m/%Y").date()
        Tere = Donante(
            "Tere",
            409998,
            fecha_nacimiento_tere,
            M,
            112324276,
            TipoSangre.O_NEGATIVO.value,
            Otamendi,
            incucai,
            fecha_fallecimiento_tere,
            [TipoOrgano.HIGADO.value, TipoOrgano.INTESTINO.value],
        )

        '''Crear receptores'''
        print(f"\n{AZUL}── Receptores ──{RESET}")

        fecha_nacimiento_zoe = datetime.strptime("14/08/2003", "%d/%m/%Y").date()
        fecha_ingreso_zoe = datetime.strptime("11/10/2006 19:00", "%d/%m/%Y %H:%M")
        Zoe = Receptor(
            "Zoe",
            46091127,
            fecha_nacimiento_zoe,
            F,
            1158141032,
            TipoSangre.A_POSITIVO.value,
            ItalianoCordoba,
            incucai,
            "higado",
            fecha_ingreso_zoe,
            TipoPatologiaHigado.CANCER.value,
            no,
        )

        fecha_nacimiento_juana = datetime.strptime("14/08/2004", "%d/%m/%Y").date()
        fecha_ingreso_juana = datetime.strptime("11/10/2008 19:00", "%d/%m/%Y %H:%M")
        Juana = Receptor(
            "Juana",
            46091128,
            fecha_nacimiento_juana,
            F,
            1145367234,
            TipoSangre.A_POSITIVO.value,
            Otamendi,
            incucai,
            "intestino",
            fecha_ingreso_juana,
            TipoPatologiaIntestino.OTRA.value,
            si
        )

        '''Crear cirujanos'''
        print(f"\n{AZUL}── Cirujanos ──{RESET}")

        print(f"\n{AZUL}── Cirujanos ──{RESET}")
        Pepe = CirujanoGeneral(
            "Pepe", 334, ItalianoCordoba, incucai
        )

        Juan = CirujanoEspecializado(
            "Juan", 888, Especialidad.GASTROENTEROLOGO.value, Favaloro, incucai
        )
        print(
            f"\n{AZUL}═════════════════════════════════════════════════════════════════════{RESET}"
        )
     