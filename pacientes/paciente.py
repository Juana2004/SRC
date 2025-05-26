from datetime import datetime
from clases_type.datos_personales import DatosPersonales
from localizables.centro_de_salud import CentroDeSalud



class Paciente:
    def __init__(self, datos: DatosPersonales, tipo_sangre: str, centro:CentroDeSalud ,incucai):
        self.nombre= datos.nombre
        self.dni= datos.dni
        self.sexo= datos.sexo
        self.telefono =datos.telefono
        self.fecha_nacimiento= datos.fecha_nacimiento
        self.datos= datos
        self.centro = centro
        self.tipo_sangre = tipo_sangre
        self.incucai = incucai


    def __eq__(self, other):
        if isinstance(other, Paciente):
            return self.datos.dni == other.datos.dni
        return False
