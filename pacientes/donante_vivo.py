from pacientes.paciente import Paciente

class DonanteVivo(Paciente):
    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai, organos_d: list):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)
        self.organos_d = organos_d
        self.fecha_abl = None
        self.hora_abl = None
        incucai.registrar_donante(self)