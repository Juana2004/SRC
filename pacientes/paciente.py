from datetime import datetime
from clases_type.datos_personales import DatosPersonales
from localizables.centro_de_salud import CentroDeSalud
from abc import ABC



class Paciente(ABC):
    def __init__(self, datos: DatosPersonales, tipo_sangre: str, centro:CentroDeSalud ):
        if type(self) is Paciente:
            raise TypeError("Vehiculo es una clase abstracta y no puede ser instanciada directamente.")
        self.nombre= datos.nombre
        self.dni= datos.dni
        self.sexo= datos.sexo
        self.telefono =datos.telefono
        self.fecha_nacimiento= datos.fecha_nacimiento
        self.datos= datos
        self.centro = centro
        self.tipo_sangre = tipo_sangre
        self.incucai = centro.incucai


    def __eq__(self, other):
        '''
        Utilizando un metodo magico compara si dos pacientes tienen igual dni
        Args:
            Other: Paciente
        Returns:
            Bool
        '''
        if isinstance(other, Paciente):
            return self.datos.dni == other.datos.dni
        return False
