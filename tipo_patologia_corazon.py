from enum import Enum
 
class Tipo_Patologia_Corazon(Enum):
    """Enumeración para patologias con sus organos correspondientes"""
    INSUFICIENCIA_C ="prioridad alta" #corazon,alta prioridad
    CONGENITAS = "prioridad alta" #corazon, alta prioridad
    ISQUEMICA = "proridad media" #corazon, prioridad media
    OTRA= "prioridad baja"