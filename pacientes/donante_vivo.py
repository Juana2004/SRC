from .paciente import Paciente
from organos.organo_vivo import OrganoVivo
from datetime import datetime, date
from excepciones import ErrorDNIRepetido, ErrorCentroNoRegistrado



class DonanteVivo(Paciente):


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
        organos_donante: list[OrganoVivo],
    ):
        super().__init__(
            nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro, incucai
        )
        self.fecha_abl = None
        self.hora_abl = None
        self.organos_donante = [OrganoVivo(tipo, incucai) for tipo in organos_donante]

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
