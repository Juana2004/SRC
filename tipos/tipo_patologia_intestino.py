from enum import Enum
 
class TipoPatologiaIntestino(Enum):
    ISQUEMIA= "prioridad alta" #intestino, muy alta prioridad
    FALLO= "prioridad alta" #intestino, alta prioridad
    OTRA ="prioridad baja"