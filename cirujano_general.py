from cirujano import Cirujano

class Cirujano_general(Cirujano):
    def __init__(self, nombre, dni, fecha_nac, sexo, tel, especialidad, centro):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, especialidad, centro)
        

