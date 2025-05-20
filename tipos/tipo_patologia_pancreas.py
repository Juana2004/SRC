from enum import Enum
 
class TipoPatologiaPancreas(Enum):
    DIABETES= "prioridad alta" #pancreas, prioridad alta
    PANCREATITIS= "prioridad media" #pancreas, prioridad media
    OTRA= "prioridad baja"