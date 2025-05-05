from paciente import Paciente



class Receptor(Paciente):

    
    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, organo_r, fecha_lista, patologia, estado):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro)
        self.organo_r = organo_r
        self.fecha_lista = fecha_lista
        self.patologia = patologia
        self.estado = estado.lower()  # 'estable' o 'inestable'

    def prioridad(self):
        if self.estado == 'estable':
            return 2
        else: 
            return 1

    def __str__(self):
        return f"RECEPTOR {self.nombre} - Órgano: {self.organo_r} - Estado: {self.estado}"
