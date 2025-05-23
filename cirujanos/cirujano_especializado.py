from cirujanos.cirujano import Cirujano
from excepciones import ErrorCedulaRepetido, ErrorCentroNoRegistrado, ErrorTipoDatoInvalido




class CirujanoEspecializado(Cirujano):

    
    def __init__(
        self, 
        nombre: str, 
        cedula: int, 
        especialidad: str,
        centro: object, 
        incucai
    ):
        super().__init__(nombre, cedula, centro, incucai)
        self.especialidad: str = especialidad
        self.operaciones_realizadas_hoy: int = 0
        try:
            incucai.registrar_cirujano_especializado(self)
        except (ErrorCedulaRepetido, ErrorCentroNoRegistrado, ErrorTipoDatoInvalido) as e:
            print(e)
        