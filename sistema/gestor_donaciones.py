from datetime import datetime
from typing import  Tuple, Optional
from pacientes.donante_vivo import DonanteVivo
from sistema.gestor_cirujanos import GestorCirujanos

class GestorDonaciones:
    """Gestiona el proceso de donación"""
    
    def __init__(self, incucai):
        self.incucai = incucai
        self._donantes_por_sangre = {}
        self._receptores_por_organo = {}
        self.gestor_cirujanos = GestorCirujanos(self)
        
    def actualizar_indices(self):
        self._donantes_por_sangre = {}
        self._receptores_por_organo = {}
        
        # Indexar donantes por tipo de sangre
        for donante in self.incucai.donantes:
            tipo = donante.t_sangre
            if tipo not in self._donantes_por_sangre:
                self._donantes_por_sangre[tipo] = []
            self._donantes_por_sangre[tipo].append(donante)
            
        # Indexar receptores por órgano requerido
        for receptor in self.incucai.receptores:
            organo = receptor.organo_r
            if organo not in self._receptores_por_organo:
                self._receptores_por_organo[organo] = []
            self._receptores_por_organo[organo].append(receptor)
    
    def _edad_es_compatible(self, edad_donante, edad_receptor):
        rangos = [
            ((0,12),(0,18)), #donante,receptor
            ((13,25),(10,40)),
            ((26,40),(15,55)),
            ((41,60),(30,70)),
            ((61,75),(50,80)),
            ((76,120),(60,120))
        ##agregar except aca , mi donantes ni receptor pueden tener mas de 120 anios
        ]
        for rango_donante, rango_receptor in rangos:
            if rango_donante[0]<=edad_donante<=rango_donante[1]:
                return rango_receptor[0]<=edad_receptor<=rango_receptor[1]
    
    def encontrar_donante_compatible(self, receptor) -> Tuple[Optional[object], Optional[int]]:
        """Encuentra un donante compatible con el receptor, retorna (donante, índice_organo)"""
        # filtra solo donantes con el mismo tipo de sangre
        tipo_sangre = receptor.t_sangre
        organo_requerido = receptor.organo_r
        edad_receptor = receptor.edad
        
        donantes_compatibles = self._donantes_por_sangre.get(tipo_sangre, [])
        for donante in donantes_compatibles:
            edad_donante = donante.edad
            if not self._edad_es_compatible(edad_donante,edad_receptor):
                continue
            if self.gestor_cirujanos.hay_cirujanos_en_centro(donante.centro):
                continue
            # Buscar órgano compatible
            for i, organo in enumerate(donante.organos_d):
                if organo.nombre == organo_requerido:
                    centro = donante.centro
                    cirujano = centro.cirujanos[0]
                    cirujano.operaciones_realizadas_hoy = 1
                    self.registrar_ablacion_donante_vivo(donante, organo_requerido)
                    return donante, i
        
        return None, None
        
    def registrar_ablacion_donante_vivo(self, donante, organo_requerido):
        """Registra la fecha de ablación para un donante vivo"""
        
        if isinstance(donante, DonanteVivo):
            fecha_actual = datetime.now()
            donante.fecha_abl = fecha_actual
            donante.hora_abl = fecha_actual.time()
            
            # Marcar el órgano específico
            for organo in donante.organos_d:
                if organo.nombre == organo_requerido:
                    organo.ablacion = fecha_actual
                    break