from pacientes.paciente import Paciente
from datetime import datetime, date
from excepciones import *
from clases_type.datos_personales import DatosPersonales
from localizables.centro_de_salud import CentroDeSalud


class Receptor(Paciente):
    def __init__(self, datos: DatosPersonales, tipo_sangre:str , centro:CentroDeSalud , organo_receptor: str, fecha_lista: datetime, patologia: str, urgencia: str):
        super().__init__(datos, tipo_sangre, centro)

        self.organo_receptor = organo_receptor
        self.fecha_lista = fecha_lista
        self.patologia = patologia
        self.urgencia = urgencia
        self.estado = "estable"

        today = date.today()
        self.edad = (
            today.year
            - datos.fecha_nacimiento.year
            - (
                (today.month, today.day)
                < (datos.fecha_nacimiento.month, datos.fecha_nacimiento.day)
            )
        )

        try:
            self.incucai.registrar_receptor(self)
        except (ErrorDNIRepetido, ErrorCentroNoRegistrado, ErrorTipoDatoInvalido) as e:
            print(e)

    def prioridad(self) -> int:
        '''
        Se asigna un valor basandose en la gravedad de la patologia y este aumenta si hay una urgencia.
        Returns:
            Entero
        '''
        base = {"prioridad baja": 1, "prioridad media": 2, "prioridad alta": 3}.get(
            self.patologia.lower(), 1
        )

        return base + 3 if self.urgencia else base

    def __lt__(self, other) -> bool:
        '''
        Compara dos receptores para definir cual tiene mayor prioridad.
        Args:
            other: Receptor
        Returns:
            Bool
        '''
        if self.estado == "inestable" and other.estado != "inestable":
            return True
        if self.estado != "inestable" and other.estado == "inestable":
            return False

        if self.prioridad() > other.prioridad():
            return True
        if self.prioridad() < other.prioridad():
            return False

        return self.fecha_lista < other.fecha_lista
