class Paciente():


    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai):
        self.nombre = nombre
        self.dni = dni
        self.fecha_nac = fecha_nac
        self.sexo = sexo
        self.tel = tel
        self.t_sangre = t_sangre
        self.centro = centro  # clase CentroSalud
        
##METODO MAGICO 4!!!
    def __eq__(self, other):
        if isinstance(other, Paciente):
            return self.dni == other.dni
        return False
  
