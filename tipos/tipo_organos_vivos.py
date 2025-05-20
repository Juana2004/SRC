from enum import Enum

class TipoOrganoVivo(Enum):
    """Enumeración para tipos de órganos que se pueden donar en vida"""
    PULMON = "pulmon"
    HIGADO = "higado"
    RINION = "rinion"
    PANCREAS = "pancreas"
    INTESTINO = "intestino"
    PIEL = "piel"