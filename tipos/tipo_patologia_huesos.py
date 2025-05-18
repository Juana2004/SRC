from enum import Enum
 
class TipoPatologiaHuesos(Enum):
     TUMOR= "prioridad alta" #huesos, prioridad alta
     FRACTURA= "prioridad media" #huesos, prioridad media
     OTRA= "prioridad baja"