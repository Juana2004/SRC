from .paciente import Paciente
from organos.organo import Organo
from datetime import datetime, date
from excepciones import ErrorDNIRepetido, ErrorCentroNoRegistrado, ErrorTipoDatoInvalido



class Donante(Paciente):


    def __init__(self, datos, tipo_sangre, centro, incucai, fecha_fallecimiento, organos_donante):
        super().__init__(datos, tipo_sangre, centro, incucai)
        self.fecha_fallecimiento = fecha_fallecimiento.date()
        self.hora_fallecimiento = fecha_fallecimiento.time()
        self.fecha_ablacion = fecha_fallecimiento.date()
        self.hora_ablacion = (
            fecha_fallecimiento.time()  # Los organos se extraen cuando el donante fallece
        )
        self.organos_donante = [
            Organo(tipo, fecha_fallecimiento, incucai) for tipo in organos_donante
        ]

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
            incucai.registrar_donante(self)
        except (ErrorDNIRepetido, ErrorCentroNoRegistrado,ErrorTipoDatoInvalido) as e:
            print(e)
