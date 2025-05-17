from receptor import Receptor
from donante import Donante
from centro_de_salud import CentroDeSalud
from cirujano_especial import Cirujano_especial
from vehiculos_terrestres import VehiculoTerrestre
from helicoptero import Helicoptero
from datetime import datetime
from avion import Avion
from incucai import INCUCAI
from organo import Organo

class Registros():
    def __init__(self):
        pass

    def Registrar(self):   
        incucai = INCUCAI()


        fecha_nacimiento = datetime.strptime("14/8/2004", "%d/%m/%Y").date()
        fecha_ingreso = datetime.strptime("11/10/2006 19:00", "%d/%m/%Y %H:%M")
        fecha_ingreso2 = datetime.strptime("10/10/2008 18:00", "%d/%m/%Y %H:%M")
        fecha_fallecimiento = datetime.strptime("17/5/2025 13:30", "%d/%m/%Y %H:%M")


        print("\n-------------Registros------------")
        # Crear centros de salud
        Otamendi = CentroDeSalud("Otamendi", "Callao 3000", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        Favaloro = CentroDeSalud("Favaloro", "Sarmiento 1855", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        ItalianoCordoba = CentroDeSalud("Italiano de Cordoba", "Roma 550", "General paz", "Cordoba", "Argentina", incucai)

        # Crear vehiculos
        Ambulancia = VehiculoTerrestre(20, "Corrientes 200", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        Ambulancia2 = VehiculoTerrestre(40, "Corrientes 200", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        Avion1 = Avion(100, "Callao 2500", "Ciudad Autonoma de Buenos Aires", "Buenos Aires", "Argentina", incucai)
        Helicoptero1 = Helicoptero(300, "Roma 550", "General paz", "Cordoba", "Argentina", incucai)

        #crear organo
        Higado1=Organo("higado", fecha_fallecimiento, incucai)
        Higado2=Organo("higado", fecha_fallecimiento, incucai)
        Corazon1=Organo("corazon", fecha_fallecimiento, incucai)
        Corazon2=Organo("corazon", fecha_fallecimiento, incucai)
        

        #crear receptores
        Juana = Receptor("Juana", 46091128, fecha_nacimiento, "femenino", 1158141032, "A+", Otamendi,incucai, "corazon", fecha_ingreso, "cancer", "estable")
        Zoe = Receptor("Zoe", 46091127, fecha_nacimiento, "femenino", 1158141032, "A+", Otamendi, incucai, "higado", fecha_ingreso2, "cancer", "inestable")

        #crear donantes
        Cami = Donante("Cami", 4600914, fecha_nacimiento, "femenino", 1158143232, "A+", Favaloro, incucai, fecha_fallecimiento, [Higado1, Corazon2])
        Tere = Donante("Tere", 4600912, fecha_nacimiento, "femenino", 1158143232, "A+", Favaloro, incucai, fecha_fallecimiento, [Higado2, Corazon1])

        #crear cirujanos
        Juan = Cirujano_especial("Juan", 445, "gastroenterologo", Otamendi, incucai)
        Carlos = Cirujano_especial("Carlos", 334, "gastroenterologo", ItalianoCordoba, incucai)

        print("\n-----------------------------------------")

        incucai.mostrar_lista_espera()
        incucai.match()
        incucai.mostrar_estado()
