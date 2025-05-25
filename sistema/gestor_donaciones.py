from datetime import datetime
from typing import Tuple, Optional
from pacientes.donante_vivo import DonanteVivo
from sistema.gestor_cirujanos import GestorCirujanos
from sistema.compatibilidad import Compatibilidad


class GestorDonaciones:

    def __init__(self, incucai):
        self.incucai = incucai
        self.gestor_cirujanos = GestorCirujanos(self)

    def compatibilidad(self, receptor: object)-> list[Tuple[object, int]]:
        donantes = self.incucai.donantes
        organo_receptor = receptor.organo_receptor
        donantes_compatibles = []

        for donante in donantes:
            edad_compatible = Compatibilidad.edad_es_compatible(donante.edad, receptor.edad)
            sangre_compatible = Compatibilidad.sangre_es_compatible(donante, receptor)
            organo_compatible = Compatibilidad.organo_es_compatible(donante, organo_receptor)

            if sangre_compatible and edad_compatible and organo_compatible is not None:
                donantes_compatibles.append((donante, organo_compatible))

        return donantes_compatibles

        
    def registrar_ablacion_donante_vivo(self, donante: object, organo_requerido: str):
        if isinstance(donante, DonanteVivo):
            fecha_actual = datetime.now()
            donante.fecha_ablacion = fecha_actual
            donante.hora_ablacion = fecha_actual.time()

            for organo in donante.organos_donante:
                if organo.nombre == organo_requerido:
                    organo.fecha_ablacion = fecha_actual
                    organo.hora_ablacion = fecha_actual.time()
                    break
