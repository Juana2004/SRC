from cirujanos.cirujano import Cirujano
from excepciones import *


class CirujanoEspecializado(Cirujano):

    def __init__(
        self, nombre: str, cedula: int, especialidad: str, centro: object
    ):
        super().__init__(nombre, cedula, centro)
        self.especialidad: str = especialidad
        self.operaciones_realizadas_hoy: int = 0
        try:
            self.incucai.registrar_cirujano_especializado(self)
        except (
            ErrorCedulaRepetido,
            ErrorCentroNoRegistrado,
            ErrorTipoDatoInvalido,
        ) as e:
            print(e)
