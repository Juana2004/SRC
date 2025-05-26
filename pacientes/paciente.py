from datetime import datetime
from clases_type.datos_personales import DatosPersonales



class Paciente:
    def __init__(self, datos: DatosPersonales, tipo_sangre: str, centro,incucai):
        self.nombre=datos.nombre
        self.dni=datos.dni
        self.fecha_nacimiento=datos.fecha_nacimiento
        self.sexo=datos.sexo
        self.telefono=datos.telefono
        self.centro = centro
        self.tipo_sangre = tipo_sangre
        self.incucai = incucai


    def __eq__(self, other):
        if isinstance(other, Paciente):
            return self.dni == other.dni
        return False
