from enum import Enum
 
class TipoPatologiaCorazon(Enum):
    """Enumeración para patologias con sus organos correspondientes"""
    INSUFICIENCIA ="prioridad alta" 
    CONGENITAS = "prioridad alta" 
    ISQUEMICA = "proridad media" 
    OTRA= "prioridad baja"

class TipoPatologiaCorneas(Enum):
    CEGUERA= "prioridad alta" 
    DEFORMIDAD= "prioridad media" 
    OTRA= "prioridad baja"

class TipoPatologiaHigado(Enum):
    HEPATITIS= "prioridad alta" 
    CANCER= "prioridad alta" 
    CIRROSIS= "prioiridad media" 
    OTRA ="prioridad baja"

class TipoPatologiaHuesos(Enum):
     TUMOR= "prioridad alta" 
     FRACTURA= "prioridad media" 
     OTRA= "prioridad baja"

class TipoPatologiaIntestino(Enum):
    ISQUEMIA= "prioridad alta" 
    FALLO= "prioridad alta" 
    OTRA ="prioridad baja"

class TipoPatologiaPancreas(Enum):
    DIABETES= "prioridad alta" 
    PANCREATITIS= "prioridad media" 
    OTRA= "prioridad baja"

class TipoPatologiaPiel(Enum):
    QUEMADURA= "prioridad alta" 
    INFECCION= "prioridad media" 
    OTRA= "prioridad baja"

class TipoPatologiaPulmon(Enum):
    FIBROSIS= "prioridad alta" 
    EPOC= "prioridad media" 
    OTRA= "prioridad baja"

class TipoPatologiaRinion(Enum):
    INSUFICIENCIA ="prioridad alta" 
    GENETICAS= "prioridad media" 
    OTRA = "prioridad baja"