class Cirujano:


    def __init__(
        self, 
        nombre: str, 
        cedula: int, 
        centro: object
    ):
        self.nombre = nombre
        self.cedula = cedula
        self.centro = centro
        self.incucai = centro.incucai
 

    def __eq__(self, other):
            if isinstance(other, Cirujano):
                return self.cedula == other.cedula
            return False