from pacientes.paciente import Paciente
from datetime import datetime, date
from excepciones import ErrorDNIRepetido, ErrorCentroNoRegistrado

class Receptor(Paciente):
    
    def __init__(self, nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai,
                 organo_r, fecha_lista, patologia, urgencia):
        super().__init__(nombre, dni, fecha_nac, sexo, tel, t_sangre, centro, incucai)

        self.organo_r = organo_r
        self.fecha_lista = fecha_lista
        self.patologia = patologia
        self.accidente = urgencia
        self.estado = "estable"

        # Procesar edad correctamente
        if isinstance(fecha_nac, str):
            fecha_nac_date = datetime.strptime(fecha_nac, "%d/%m/%Y").date()
        else:
            fecha_nac_date = fecha_nac

        today = date.today()
        self.edad = today.year - fecha_nac_date.year - (
            (today.month, today.day) < (fecha_nac_date.month, fecha_nac_date.day)
        )

        try:
            incucai.registrar_receptor(self)
        except (ErrorDNIRepetido, ErrorCentroNoRegistrado) as e:
            print(e)



    def prioridad(self):
        base = {
            "prioridad baja": 1,
            "prioridad media": 2,
            "prioridad alta": 3
        }.get(self.patologia.lower(), 1)

        return base + 3 if self.accidente else base

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

