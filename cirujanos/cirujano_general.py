from cirujanos.cirujano import Cirujano

class Cirujano_general(Cirujano):
    def __init__(self, nombre, dni, centro, incucai):
        super().__init__(nombre, dni, centro, incucai)
        self.operaciones_realizadas_hoy = 0
        incucai.registrar_cirujano_gen(self)