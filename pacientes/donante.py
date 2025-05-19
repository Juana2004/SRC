from pacientes.paciente import Paciente
from organos.organo import Organo
from datetime import datetime, date
class Donante(Paciente):


    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai, fecha_fallec, organos_d: list):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)
        self.fecha_fallec = fecha_fallec.date()
        self.hora_fallec = fecha_fallec.time()
        self.fecha_abl = fecha_fallec.date()
        self.hora_abl = fecha_fallec.time() ##los organos se extraen a los minutos q el paciente muere
        self.organos_d = [Organo(tipo,fecha_fallec, incucai) for tipo in organos_d]
          # Aceptar tanto string como date
        if isinstance(fecha_nac, str):
            fecha_nac_date = datetime.strptime(fecha_nac, "%d/%m/%Y").date()
        else:
            fecha_nac_date = fecha_nac

        today = date.today()
        self.edad = today.year - fecha_nac_date.year - ((today.month, today.day) < (fecha_nac_date.month, fecha_nac_date.day))
        
        incucai.registrar_donante(self)
