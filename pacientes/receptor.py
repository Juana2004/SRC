from pacientes.paciente import Paciente
from datetime import datetime, date
from excepciones import ErrorDNIRepetido, ErrorCentroNoRegistrado



class Receptor(Paciente):


    def __init__(
        self,
        nombre: str,
        dni: int,
        fecha_nacimiento: datetime.date,
        sexo: str,
        telefono: int,
        tipo_sangre: str,
        centro: object,
        incucai,  # Instancia de la clase incucai
        organo_receptor: str,
        fecha_lista: datetime,
        patologia: str,
        urgencia: str,
    ):
        super().__init__(
            nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro, incucai
        )

        self.organo_receptor = organo_receptor
        self.fecha_lista = fecha_lista
        self.patologia = patologia
        self.urgencia = urgencia
        self.estado = "estable"

        today = date.today()
        self.edad = (
            today.year
            - fecha_nacimiento.year
            - (
                (today.month, today.day)
                < (fecha_nacimiento.month, fecha_nacimiento.day)
            )
        )

        try:
            incucai.registrar_receptor(self)
        except (ErrorDNIRepetido, ErrorCentroNoRegistrado) as e:
            print(e)

    def prioridad(self):
        base = {"prioridad baja": 1, "prioridad media": 2, "prioridad alta": 3}.get(
            self.patologia.lower(), 1
        )

        return base + 3 if self.urgencia else base

    def __lt__(self, other):
        # 1. Primero priorizamos por estado clínico
        if self.estado == "inestable" and other.estado != "inestable":
            return True
        if self.estado != "inestable" and other.estado == "inestable":
            return False

        # 2. Luego por mayor prioridad (número más alto)
        if self.prioridad() > other.prioridad():
            return True
        if self.prioridad() < other.prioridad():
            return False

        # 3. Finalmente, por fecha de ingreso a lista (más antiguo primero)
        return self.fecha_lista < other.fecha_lista
