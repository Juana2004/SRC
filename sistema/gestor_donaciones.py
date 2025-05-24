from datetime import datetime
from typing import Tuple, Optional
from pacientes.donante_vivo import DonanteVivo
from sistema.gestor_cirujanos import GestorCirujanos
from tipos.tipo_sangre import TipoSangre


class GestorDonaciones:
    """Gestiona el proceso de donación"""

    def __init__(self, incucai):
        self.incucai = incucai
        self.gestor_cirujanos = GestorCirujanos(self)

    def _edad_es_compatible(self, edad_donante, edad_receptor):
        rangos = [
            ((0, 12), (0, 18)),    # (rango_donante), (rango_receptor)
            ((13, 25), (10, 40)),
            ((26, 40), (15, 55)),
            ((41, 60), (30, 70)),
            ((61, 75), (50, 80)),
            ((76, 120), (60, 120)),
        ]
        
        for (min_don, max_don), (min_rec, max_rec) in rangos:
            # Verificar si la edad del donante está en el rango del donante
            if min_don <= edad_donante <= max_don and min_rec <= edad_receptor <= max_rec:
                # Si está en el rango, verificar si el receptor está en el rango correspondiente
                return True
        
        return False

    
    def _sangre_es_compatible(self, donante, receptor) -> bool:
        sangre_donante = donante.tipo_sangre
        sangre_receptor = receptor.tipo_sangre

        compatibilidad = [
            (TipoSangre.O_NEGATIVO.value, [TipoSangre.O_NEGATIVO.value]),
            (TipoSangre.O_POSITIVO.value, [TipoSangre.O_POSITIVO.value, TipoSangre.O_NEGATIVO.value]),
            (TipoSangre.A_NEGATIVO.value, [TipoSangre.A_NEGATIVO.value, TipoSangre.O_NEGATIVO.value]),
            (TipoSangre.A_POSITIVO.value, [TipoSangre.A_POSITIVO.value, TipoSangre.A_NEGATIVO.value, TipoSangre.O_POSITIVO.value, TipoSangre.O_NEGATIVO.value]),
            (TipoSangre.B_NEGATIVO.value, [TipoSangre.B_NEGATIVO.value, TipoSangre.O_NEGATIVO.value]),
            (TipoSangre.B_POSITIVO.value, [TipoSangre.B_POSITIVO.value, TipoSangre.B_NEGATIVO.value, TipoSangre.O_POSITIVO.value, TipoSangre.O_NEGATIVO.value]),
            (TipoSangre.AB_NEGATIVO.value, [TipoSangre.AB_NEGATIVO.value, TipoSangre.A_NEGATIVO.value, TipoSangre.B_NEGATIVO.value, TipoSangre.O_NEGATIVO.value]),
            (TipoSangre.AB_POSITIVO.value, [
                TipoSangre.AB_POSITIVO.value, TipoSangre.AB_NEGATIVO.value,
                TipoSangre.A_POSITIVO.value, TipoSangre.A_NEGATIVO.value,
                TipoSangre.B_POSITIVO.value, TipoSangre.B_NEGATIVO.value,
                TipoSangre.O_POSITIVO.value, TipoSangre.O_NEGATIVO.value,
            ]),
        ]

        
        compatibles = []
        for receptor_tipo, donantes_compatibles in compatibilidad:
            if receptor_tipo == sangre_receptor:
                compatibles = donantes_compatibles
                break

        return any(sangre_donante == d for d in compatibles)


    def encontrar_donante_compatible(
        self, receptor: object
    ) -> Tuple[Optional[object], Optional[int]]:
        """Encuentra un donante compatible con el receptor, retorna (donante, índice_organo)"""

        organo_requerido = receptor.organo_receptor
        edad_receptor = receptor.edad
        donantes = self.incucai.donantes
 
        donantes_compatibles = []
        for donante in donantes:
            if self._sangre_es_compatible(donante, receptor):
                donantes_compatibles.append(donante)

        if not donantes_compatibles:
            return None, None

        for donante in donantes_compatibles:
            edad_donante = donante.edad
            if not self._edad_es_compatible(edad_donante, edad_receptor):
                continue
            if not self.gestor_cirujanos.hay_cirujanos_en_centro(donante.centro):
                continue

            for i, organo in enumerate(donante.organos_donante):
                if organo.nombre == organo_requerido:
                    centro = donante.centro
                    cirujano = centro.cirujanos[0]
                    print(f"El cirujano {cirujano.nombre} realiza la ablacion")
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

            
            for organo in donante.organos_donante:
                if organo.nombre == organo_requerido:
                    organo.ablacion = fecha_actual
                    break
