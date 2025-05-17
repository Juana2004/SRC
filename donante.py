from paciente import Paciente

class Donante(Paciente):


    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai, fecha_fallec, organos_d: list):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)
        self.fecha_fallec = fecha_fallec.date()
        self.hora_fallec = fecha_fallec.time()
        self.fecha_abl = fecha_fallec.date()
        self.hora_abl = fecha_fallec.time() ##los organos se extraen a los minutos q el paciente muere
        self.organos_d = organos_d  # lista

        incucai.registrar_donante(self)
