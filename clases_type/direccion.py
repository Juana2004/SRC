from dataclasses import dataclass


@dataclass
class Direccion:
    direccion: str
    partido: str
    provincia: str
    pais: str
