class Cirujano:


    def __init__(
        self, 
        nombre: str, 
        cedula: int, 
        centro: object, 
        incucai
    ):
        self.nombre = nombre
        self.cedula = cedula
        self.centro = centro
 

    def __eq__(self, other):
            if isinstance(other, Cirujano):
                return self.cedula == other.cedula
            return False