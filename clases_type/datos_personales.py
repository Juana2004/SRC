from dataclasses import dataclass
from datetime import datetime



@dataclass
class DatosPersonales:
    nombre: str
    dni: int 
    fecha_nacimiento: datetime
    sexo: str
    telefono: int