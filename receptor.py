from paciente import Paciente


class Receptor(Paciente):

    
    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai, organo_r, fecha_lista, patologia, estado):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)
        self.organo_r = organo_r
        self.fecha_lista = fecha_lista
        self.patologia = patologia
        self.estado = estado.lower()  # 'estable' o 'inestable'

        incucai.registrar_receptor(self)

    def prioridad(self):
        if self.estado == 'estable':
            return 2
        else: 
            return 1

