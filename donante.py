from paciente import Paciente

class Donante(Paciente):


    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai, fecha_fallec, hora_fallec, fecha_abl, hora_abl, organos_d):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)
        self.fecha_fallec = fecha_fallec
        self.hora_fallec = hora_fallec
        self.fecha_abl = fecha_abl
        self.hora_abl = hora_abl
        self.organos_d = organos_d  # lista

        incucai.registrar_donante(self)
