from pacientes.paciente import Paciente
from organos.organoo import Organoo

class DonanteVivo(Paciente):
    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai, organos_d: list):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)
        self.fecha_abl = None
        self.hora_abl = None
        self.organos_d = [Organoo(tipo, incucai) for tipo in organos_d]
        incucai.registrar_donante(self)