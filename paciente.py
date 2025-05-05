from persona import Persona



class Paciente(Persona):


    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro):
        super().__init__(nombre, dni, fecha_nac, t_sangre)
        self.sexo = sexo
        self.tel = tel
        self.centro = centro  # clase CentroSalud

    def __str__(self):
        return f"{self.nombre} (DNI: {self.dni}) - Centro: {self.centro}"
