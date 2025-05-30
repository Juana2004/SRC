from abc import ABC
class Cirujano(ABC):


    def __init__(
        self, 
        nombre: str, 
        cedula: int, 
        centro: object
    ):
        if type(self) is Cirujano:
            raise TypeError("Vehiculo es una clase abstracta y no puede ser instanciada directamente.")
        self.nombre = nombre
        self.cedula = cedula
        self.centro = centro
        self.incucai = centro.incucai
 

    def __eq__(self, other):
            if isinstance(other, Cirujano):
                return self.cedula == other.cedula
            return False