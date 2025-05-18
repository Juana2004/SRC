from datetime import datetime
from typing import  Tuple, Optional

class GestorDonaciones:
    """Gestiona el proceso de donación"""
    
    def __init__(self, incucai):
        self.incucai = incucai
        self._donantes_por_sangre = {}
        self._receptores_por_organo = {}
        
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
    
    def encontrar_donante_compatible(self, receptor) -> Tuple[Optional[object], Optional[int]]:
        """Encuentra un donante compatible con el receptor, retorna (donante, índice_organo)"""
        # filtra solo donantes con el mismo tipo de sangre
        tipo_sangre = receptor.t_sangre
        organo_requerido = receptor.organo_r
        
        donantes_compatibles = self._donantes_por_sangre.get(tipo_sangre, [])
        
        for donante in donantes_compatibles:
            # Buscar órgano compatible
            for i, organo in enumerate(donante.organos_d):
                if organo.nombre == organo_requerido:
                    return donante, i
        
        return None, None
        
    def registrar_ablacion_donante_vivo(self, donante, organo_requerido):
        """Registra la fecha de ablación para un donante vivo"""
        from pacientes.donante_vivo import DonanteVivo
        
        if isinstance(donante, DonanteVivo):
            fecha_actual = datetime.now()
            donante.fecha_abl = fecha_actual
            donante.hora_abl = fecha_actual.time()
            
            # Marcar el órgano específico
            for organo in donante.organos_d:
                if organo.nombre == organo_requerido:
                    organo.ablacion = fecha_actual
                    break