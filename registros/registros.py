from datetime import datetime

from pacientes.receptor import Receptor
from pacientes.donante import Donante
from pacientes.donante_vivo import DonanteVivo
from pacientes.paciente import Paciente

from cirujanos.cirujano_especializado import CirujanoEspecializado
from cirujanos.cirujano_general import CirujanoGeneral

from localizables.centro_de_salud import CentroDeSalud
from localizables.vehiculos_terrestres import VehiculoTerrestre
from localizables.helicoptero import Helicoptero
from localizables.avion import Avion
from clases_type.direccion import Direccion

from tipos.tipo_especialidad import Especialidad
from tipos.tipo_organo import TipoOrgano
from tipos.tipo_organos_vivos import TipoOrganoVivo
from tipos.tipo_sangre import TipoSangre
from tipos.patologias import *

from clases_type.datos_personales import DatosPersonales

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

        """Crear centros de salud"""
        print(f"\n{AZUL}── Centros de salud ──{RESET}")

        direccion_otamendi = Direccion("Azcuenaga 870",
            "Ciudad Autonoma de Buenos Aires",
            "Buenos Aires",
            "Argentina",)
        Otamendi = CentroDeSalud(
            "Otamendi",
            direccion_otamendi,
            incucai,
        )

        direccion_favaloro = Direccion("Av. Belgrano 1746",
            "Ciudad Autonoma de Buenos Aires",
            "Buenos Aires",
            "Argentina")
        Favaloro = CentroDeSalud(
            "Favaloro",
            direccion_favaloro,
            incucai,
        )

        direccion_italianocordoba = Direccion("Roma 550",
            "General paz",
            "Cordoba",
            "Argentina")
        ItalianoCordoba = CentroDeSalud(
            "Italiano de Cordoba",
            direccion_italianocordoba,
            incucai,
        )

        """ Crear vehículos"""
        print(f"\n{AZUL}── Vehículos terrestres ──{RESET}")
        direccion_ambulancia2 = Direccion("Corrientes 200",
            "Ciudad Autonoma de Buenos Aires",
            "Buenos Aires",
            "Argentina")
        Ambulancia2 = VehiculoTerrestre(
            "Ambulancia",
            40,
            direccion_ambulancia2,
            Favaloro,
            incucai,
        )
    
        print(f"\n{AZUL}── Aviones ──{RESET}")

        direccion_avion1 = Direccion("Chacabuco 2000",
            "Carlos Paz",
            "Cordoba",
            "Argentina")
        Avion1 = Avion(
            "avion",
            700,
            direccion_avion1,
            ItalianoCordoba,
            incucai,
        )
        direccion_avion2 = Direccion("Chacabuco 2000",
            "Carlos Paz",
            "Cordoba",
            "Argentina",)
        Avion2 = Avion(
            "avion2",
            900,
            direccion_avion2,
            Favaloro,
            incucai,
        )

        print(f"\n{AZUL}── Helicópteros ──{RESET}")

        direccion_helicoptero1 = Direccion("Roma 550",
            "General paz",
            "Cordoba",
            "Argentina")
        
        Helicoptero1 = Helicoptero(
            "helicoptero",
            300,
            direccion_helicoptero1
            ,
            Favaloro,
            incucai,
        )
        
        print(f"\n{AZUL}── Donantes ──{RESET}")


        '''fecha_nacimiento_carlos = datetime.strptime("14/05/2002", "%d/%m/%Y").date()
        datos_carlos=DatosPersonales("Carlos",
            409992,
            fecha_nacimiento_carlos,
            M,
            112324256)
        Carlos = DonanteVivo(
            datos_carlos,
            TipoSangre.O_NEGATIVO.value,
            Otamendi,
            incucai,
            [TipoOrganoVivo.HIGADO.value, TipoOrganoVivo.INTESTINO.value],
        )

        fecha_fallecimiento_tere = datetime.strptime(
            "17/5/2025 13:30", "%d/%m/%Y %H:%M"
        )
        fecha_nacimiento_tere = datetime.strptime("17/5/2003", "%d/%m/%Y").date()
        datos_tere= DatosPersonales("Tere",
            409998,
            fecha_nacimiento_tere,
            M,
            112324276)
        Tere = Donante(datos_tere,
            TipoSangre.O_NEGATIVO.value,
            Otamendi,
            incucai,
            fecha_fallecimiento_tere,
            [TipoOrgano.HIGADO.value, TipoOrgano.INTESTINO.value],
        )

        fecha_fallecimiento_maria = datetime.strptime(
            "24/5/2025 11:30", "%d/%m/%Y %H:%M"
        )
        fecha_nacimiento_maria = datetime.strptime("17/5/2003", "%d/%m/%Y").date()
        datos_maria=DatosPersonales("Maria",
            409978,
            fecha_nacimiento_maria,
            M,
            112324276)
        Maria = Donante( datos_maria,
            TipoSangre.O_POSITIVO.value,
            Otamendi,
            incucai,
            fecha_fallecimiento_maria,
            [TipoOrgano.HIGADO.value, TipoOrgano.INTESTINO.value],
        )
        """Crear receptores"""
        print(f"\n{AZUL}── Receptores ──{RESET}")
'''
        fecha_nacimiento_zoe = datetime.strptime("14/08/2003", "%d/%m/%Y").date()
        fecha_ingreso_zoe = datetime.strptime("11/10/2006 19:00", "%d/%m/%Y %H:%M")
        datos_zoe=DatosPersonales("Zoe",
            46091128,
            fecha_nacimiento_zoe,
            F,
            1158141032)
        Zoe = Receptor(
            datos_zoe,
            TipoSangre.A_POSITIVO.value,
            ItalianoCordoba,
            incucai,
            TipoOrgano.HIGADO.value,
            fecha_ingreso_zoe,
            TipoPatologiaHigado.CANCER.value,
            no,
        )
        
        fecha_nacimiento_juana = datetime.strptime("14/08/2004", "%d/%m/%Y").date()
        fecha_ingreso_juana = datetime.strptime("11/10/2008 19:00", "%d/%m/%Y %H:%M")
        datos_juana=DatosPersonales("Juana",
            46091127,
            fecha_nacimiento_juana,
            F,
            1145367234)
        Juana = Receptor(
            datos_juana,
            TipoSangre.A_POSITIVO.value,
            Favaloro,
            incucai,
            TipoOrgano.INTESTINO.value,
            fecha_ingreso_juana,
            TipoPatologiaIntestino.OTRA.value,
            si,
        )
        fecha_nacimiento_juana = datetime.strptime("14/08/2004", "%d/%m/%Y").date()
        fecha_ingreso_juana = datetime.strptime("11/10/2008 19:00", "%d/%m/%Y %H:%M")
        datos_juana=DatosPersonales("Sam",
            46091127,
            fecha_nacimiento_juana,
            F,
            1145367234)
        Juana = Receptor(
            datos_juana,
            TipoSangre.A_POSITIVO.value,
            Favaloro,
            incucai,
            TipoOrgano.INTESTINO.value,
            fecha_ingreso_juana,
            TipoPatologiaIntestino.OTRA.value,
            si,
        )


        print(f"\n{AZUL}── Cirujanos ──{RESET}")
        Pepe = CirujanoGeneral("Pepe", 334, Otamendi, incucai)

        Damian = CirujanoGeneral("Damian", 394, Otamendi, incucai)

        Juan = CirujanoEspecializado(
            "Juan", 887, Especialidad.GASTROENTEROLOGO.value, Favaloro, incucai
        )
        Martin = CirujanoEspecializado(
            "Martin", 888, Especialidad.TRAUMATOLOGO.value, ItalianoCordoba, incucai
        )
        print(
            f"\n{AZUL}═════════════════════════════════════════════════════════════════════{RESET}"
        )
