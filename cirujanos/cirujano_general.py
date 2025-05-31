from .cirujano import Cirujano
from excepciones import *



class CirujanoGeneral(Cirujano):
    

    def __init__(self, nombre: str, cedula: int, centro: object):

        super().__init__(nombre, cedula, centro)
        self.operaciones_realizadas_hoy: int = 0
        try:
            self.incucai.registrar_cirujano_general(self)
        except (
            ErrorCedulaRepetido,
            ErrorCentroNoRegistrado,
            ErrorTipoDatoInvalido,
        ) as e:
            print(e)
