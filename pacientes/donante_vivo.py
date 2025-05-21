from pacientes.paciente import Paciente
from organos.organoo import Organoo
from datetime import datetime, date
from excepciones import ErrorDNIRepetido, ErrorCentroNoRegistrado


class Persona(): # Hacer!!!
    nombre: str
    

class DonanteVivo(Paciente):
    def __init__(
        self,
        nombre,
        dni,
        fecha_nac,
        sexo,
        tel,
        t_sangre,
        centro,
        incucai,
        organos_d: list,
    ):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)
        self.fecha_abl = None
        self.hora_abl = None
        self.organos_d = [Organoo(tipo, incucai) for tipo in organos_d]

        # Aceptar tanto string como date
        if isinstance(fecha_nac, str):
            fecha_nac_date = datetime.strptime(fecha_nac, "%d/%m/%Y").date()
        else:
            fecha_nac_date = fecha_nac

        today = date.today()
        self.edad = (
            today.year
            - fecha_nac_date.year
            - ((today.month, today.day) < (fecha_nac_date.month, fecha_nac_date.day))
        )

        try:
            incucai.registrar_donante(self)
        except (ErrorDNIRepetido, ErrorCentroNoRegistrado) as e:
            print(e)
