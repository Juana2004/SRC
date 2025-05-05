from receptor import Receptor
from donante import Donante
from incucai import INCUCAI
from centro_de_salud import CentroDeSalud
from cirujano import Cirujano
from vehiculos_terrestres import VehiculoTerrestre

def main():
    from datetime import datetime

    fecha_nacimiento = datetime.strptime("14/8/2004", "%d/%m/%Y").date()
    fecha_ingreso = datetime.strptime("11/10/2006", "%d/%m/%Y").date()
    fecha_ingreso2 = datetime.strptime("10/10/2008", "%d/%m/%Y").date()
    fecha_fallecimiento = datetime.strptime("20/5/2006", "%d/%m/%Y").date()
    fexha_ab = datetime.strptime("20/5/2006", "%d/%m/%Y").date()

    Otamendi = CentroDeSalud("otamendi", "Callao 3000", "CABA", "BS AS")
    Favaloro = CentroDeSalud("favaloro", "Sarmiento 20", "CABA", "BS AS")
    Ambulancia = VehiculoTerrestre(20, "Corrientes 200", "CABA", "BS AS")
    Juan = Cirujano("Juan", 30303127, "gastronterologo", Otamendi)
    incucai = INCUCAI() 
    incucai.registrar_centro(Otamendi)
    incucai.registrar_cirujano(Juan)
    incucai.registrar_vehiculo_terr(Ambulancia)

    Juana = Receptor("Juana", 46091127, fecha_nacimiento, "femenino", 1158141032, "A+", Favaloro, "higado", fecha_ingreso, "cancer", "estable")
    Zoe = Receptor("Zoe", 46091127, fecha_nacimiento, "femenino", 1158141032, "A+", Otamendi, "higado", fecha_ingreso2, "cancer", "inestable")


    incucai.registrar_receptor(Juana)  
    incucai.registrar_receptor(Zoe)
    incucai.mostrar_lista_espera()

    Cami = Donante("Cami", 4600914, fecha_nacimiento, "femenino", 1158143232, "A+", Otamendi, fecha_fallecimiento, 10, fecha_fallecimiento, 10, ["higado"])
    Tere = Donante("Tere", 4600912, fecha_nacimiento, "femenino", 1158143232, "A+", Otamendi, fecha_fallecimiento, 10, fecha_fallecimiento, 10, ["higado"])
    incucai.registrar_donante(Tere)
    incucai.registrar_donante(Cami)
    incucai.match()
    incucai.mostrar_estado()




if __name__ == "__main__":
    main()
