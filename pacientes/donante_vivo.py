from .paciente import Paciente
from organos.organo_vivo import OrganoVivo
from datetime import date
from excepciones import *
from clases_type.datos_personales import DatosPersonales
from localizables.centro_de_salud import CentroDeSalud


class DonanteVivo(Paciente):
 def __init__(self, datos: DatosPersonales, tipo_sangre:str, centro:CentroDeSalud, organos_donante: list[OrganoVivo]):
    super().__init__(datos, tipo_sangre, centro,)
    self.fecha_ablacion = None
    self.hora_ablacion = None
    self.organos_donante = [OrganoVivo(tipo, self.incucai) for tipo in organos_donante]

    today = date.today()
    self.edad = (
        today.year
        - self.datos.fecha_nacimiento.year
        - (
            (today.month, today.day)
            < (self.datos.fecha_nacimiento.month, self.datos.fecha_nacimiento.day)
        )
    )

    try:
        self.incucai.registrar_donante(self)
    except (ErrorDNIRepetido, ErrorCentroNoRegistrado, ErrorTipoDatoInvalido) as e:
        print(e)
