from enum import Enum
 
class Tipo_Patologia(Enum):
    """Enumeración para patologias con sus organos correspondientes"""
    CORAZON = "corazon"
    INSUFICIENCIA_C ="insuficiencia_c" #corazon,alta prioridad
    CONGENITAS = "congenitas" #corazon, alta prioridad
    ISQUEMICA = "isquemica" #corazon, prioridad media
    HEPATITIS= "hepatitis" #higado,muy alta prioridad
    CANCER= "cance_de_h" #higado,  alta prioridad
    CIRROSIS= "cirrosis" #higado, prioridad media
    TUMOR= "tumor" #huesos, prioridad alta
    FRACTURA= "fractura" #huesos, prioridad media
    DIABETES= "diabetes" #pancreas, prioridad alta
    PANCREATITIS= "pancreatitis" #pancreas, prioridad media
    INSUFICIENCIA_R ="insuficiencia_r" #riñon, prioridad alta
    GENETICAS= "geneticas" #riñon, prioridad media
    FIBROSIS= "fibrosis" #pulmon, prioridad alta
    EPOC= "epoc" #pulmon, prioridad media
    QUEMADURA= "quemadura" #piel, prioridad alta
    INFECCION= "infeccion" #piel, prioridad media
    CEGUERA= "ceguera" #corneas, prioridad alta
    DEFORMIDAD= "deformidad" #corneas, prioridad media