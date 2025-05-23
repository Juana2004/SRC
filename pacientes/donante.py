from .paciente import Paciente
from organos.organo import Organo
from datetime import datetime, date
from excepciones import ErrorDNIRepetido, ErrorCentroNoRegistrado



class Donante(Paciente):


    def __init__(
        self,
        nombre: str,
        dni: int,
        fecha_nacimiento: datetime.date,
        sexo: str,
        telefono: int,
        tipo_sangre: str,
        centro: object,
        incucai,  # Instancia de la clase incucai
        fecha_fallececimiento: datetime,
        organos_donante: list[Organo],
    ):
        super().__init__(
            nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro, incucai
        )
        self.fecha_fallecimiento = fecha_fallececimiento.date()
        self.hora_fallecimiento = fecha_fallececimiento.time()
        self.fecha_ablacion = fecha_fallececimiento.date()
        self.hora_ablacion = (
            fecha_fallececimiento.time()  # Los organos se extraen cuando el donante fallece
        )
        self.organos_donante = [
            Organo(tipo, fecha_fallececimiento, incucai) for tipo in organos_donante
        ]

        today = date.today()
        self.edad = (
            today.year
            - fecha_nacimiento.year
            - (
                (today.month, today.day)
                < (fecha_nacimiento.month, fecha_nacimiento.day)
            )
        )

        try:
            incucai.registrar_donante(self)
        except (ErrorDNIRepetido, ErrorCentroNoRegistrado) as e:
            print(e)
