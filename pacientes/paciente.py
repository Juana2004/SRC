from datetime import datetime


class Paciente:

    def __init__(
        self,
        nombre: str,
        dni: int,
        fecha_nacimiento: datetime.date,
        sexo: str,
        telefono: int,
        tipo_sangre: str,
        centro: object,
        incucai,
    ):
        self.nombre = nombre
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo
        self.telefono = telefono
        self.tipo_sangre = tipo_sangre
        self.centro = centro

    def __eq__(self, other):
        if isinstance(other, Paciente):
            return self.dni == other.dni
        return False
