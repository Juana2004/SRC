from enum import Enum
 
class TipoPatologiaHigado(Enum):
    HEPATITIS= "prioridad alta" #higado, muy alta prioridad
    CANCER= "prioridad alta" #higado, alta prioridad
    CIRROSIS= "prioiridad media" #higado, prioridad media
    OTRA ="prioridad baja"
    