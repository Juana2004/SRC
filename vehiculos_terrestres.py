from vehiculos import Vehiculo

class VehiculoTerrestre(Vehiculo):
    def __init__(self, velocidad, direccion, partido, provincia):
        super().__init__(velocidad, direccion, partido, provincia)
    
