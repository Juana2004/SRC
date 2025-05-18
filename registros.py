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


class Registros():
    def __init__(self):
        pass

    def Registrar(self,incucai):   

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
        ItalianoCordoba = CentroDeSalud("Italiano de Cordoba", "Roma 550", "General paz", "Cordoba", "Argentina", incucai)

        # Crear vehiculos
        Ambulancia = VehiculoTerrestre("ambulancia",20, "Corrientes 200", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        #Ambulancia2 = VehiculoTerrestre(40, "Corrientes 200", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        #Avion1 = Avion(100, "Callao 2500", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        #Helicoptero1 = Helicoptero(300, "Roma 550", "General paz", "Cordoba", "Argentina", incucai)

        #crear donantes
        Cami = Donante("Cami", 4600914, fecha_nacimiento, F, 1158143232, TipoSangre.A_POSITIVO.value, Favaloro, incucai, fecha_fallecimiento, [TipoOrgano.HIGADO.value, TipoOrgano.CORAZON.value])
        Tere = Donante("Tere", 4600912, fecha_nacimiento, F, 1158143232, TipoSangre.A_POSITIVO.value, Favaloro, incucai, fecha_fallecimiento, [TipoOrgano.HIGADO.value, TipoOrgano.CORAZON.value])
        Carlos = DonanteVivo("Carlos", 409992, fecha_nacimiento, M, 112324256, TipoSangre.A_POSITIVO.value, Favaloro, incucai, [TipoOrganoVivo.HIGADO.value])

        #crear receptores
        Juana = Receptor("Juana", 46091128, fecha_nacimiento, F, 1158141032, TipoSangre.A_POSITIVO.value, Otamendi,incucai, TipoOrgano.CORAZON.value, fecha_ingreso, TipoPatologiaCorazon.INSUFICIENCIA_C.value,si )
        Zoe = Receptor("Zoe", 46091127, fecha_nacimiento, F, 1158141032, TipoSangre.A_POSITIVO.value, Otamendi, incucai, TipoOrgano.HIGADO.value, fecha_ingreso2, TipoPatologiaHigado.HEPATITIS.value,si )

        
        #crear cirujanos
        Juan = Cirujano_especial("Juan", 445, Especialidad.GASTROENTEROLOGO.value, Otamendi, incucai)
        Pepe = Cirujano_especial("Pepe", 334, Especialidad.GASTROENTEROLOGO.value, ItalianoCordoba, incucai)
        print("\n-----------------------------------------")


