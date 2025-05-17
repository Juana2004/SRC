from enum import Enum
 
class Tipo_Patologia_Higado(Enum):
    HEPATITIS= "prioridad alta" #higado, muy alta prioridad
    CANCER= "prioridad alta" #higado, alta prioridad
    CIRROSIS= "prioiridad media" #higado, prioridad media
    OTRA ="prioridad baja"
    