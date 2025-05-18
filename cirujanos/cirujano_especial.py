from cirujano import Cirujano   

class Cirujano_especial(Cirujano):
    def __init__(self, nombre, dni, especialidad, centro, incucai):
        super().__init__(nombre, dni, centro, incucai)
        self.especialidad = especialidad
        self.operaciones_realizadas_hoy = 0
        incucai.registrar_cirujano_esp(self)