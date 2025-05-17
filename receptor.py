from paciente import Paciente


class Receptor(Paciente):

    
    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai, organo_r, fecha_lista, patologia, accidente):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)
        self.organo_r = organo_r
        self.fecha_lista = fecha_lista
        self.patologia = patologia
        if accidente == "si":
            self.accidente = True
        else:
            self.accidente = False

        incucai.registrar_receptor(self)

    def prioridad(self):
        if self.patologia == "prioridad baja" and self.accidente == False:
            return 1
        elif self.patologia == "prioridad media" and self.accidente == False:
            return 2
        elif self.patologia == "prioridad alta" and self.accidente == False:
            return 3
        elif self.patologia == "prioridad baja" and self.accidente == True:
            return 4
        elif self.patologia == "prioridad media" and self.accidente == True:
            return 5
        elif self.patologia == "prioridad alta" and self.accidente == True:
            return 6
     
