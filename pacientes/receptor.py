from pacientes.paciente import Paciente


class Receptor(Paciente):

    
    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai, organo_r, fecha_lista, patologia, accidente):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)
        self.organo_r = organo_r
        self.fecha_lista = fecha_lista
        self.patologia = patologia
        self.accidente = accidente

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
        
    def __lt__(self, other):
        """
        Define el comportamiento del operador < para ordenar receptores.
        Cuando Python ordena una lista de receptores, compara pares de objetos.
        
        Esta función devuelve True si self debe ir ANTES que other en la lista ordenada.
        
        Criterios de ordenamiento:
        1. Mayor prioridad primero (valores más altos de prioridad() van primero)
        2. A igual prioridad, se ordena por fecha (fechas más antiguas primero)
        """
        if self.prioridad() > other.prioridad():
            return True
        elif self.prioridad() == other.prioridad() and self.fecha_lista < other.fecha_lista:
            return True
        else:
            return False
