from sistema.gestor_cirujanos import GestorCirujanos
from sistema.gestor_donaciones import GestorDonaciones
from pacientes.receptor import Receptor


class Match:
    def __init__(self, incucai):
        self.incucai = incucai
        self.gestor_cirujanos = GestorCirujanos(incucai)
        self.gestor_donaciones = GestorDonaciones(incucai)

    def match(self) -> bool:
        """
        Intenta realizar un match entre receptores y donantes disponibles.
        Este método normaliza las especialidades de los cirujanos y recorre
        la lista de receptores evaluando su compatibilidad con los donantes.
        Si encuentra un donante compatible para un receptor, se coordina la operación.
        Returns:
            bool: True si se realizó al menos un match exitoso, False en caso contrario.
        """
        self.gestor_cirujanos.normalizar_especialidades()
        receptores_pendientes = list(self.incucai.receptores)
        receptores_procesados = set()
        se_realizo_match = False

        while receptores_pendientes:
            receptor = receptores_pendientes.pop(0)
            if id(receptor) in receptores_procesados:
                continue

            print(f"\nEvaluando receptor: {receptor.nombre}\n")

            if not self._hay_cirujanos_en_centro(receptor):
                continue

            donantes_compatibles = self.gestor_donaciones.compatibilidad(receptor)

            if not donantes_compatibles:
                print(f"❌ No se encontró donante compatible para {receptor.nombre}")
                continue

            if self.gestor_donaciones.procesar_donantes(
                donantes_compatibles, receptor, receptores_pendientes
            ):
                se_realizo_match = True
                receptores_procesados.add(id(receptor))
            else:
                print(f"\n❌ No se pudo realizar match para {receptor.nombre}\n")

        return se_realizo_match

    def _hay_cirujanos_en_centro(self, receptor: Receptor) -> bool:
        '''
        Invoca al metodo ya existente encargado de verficar si hay al menos un cirujano disponible en el centro del receptor e 
            informa si no lo hay.
        Args:
            receptor: Receptor 
        Returns:
            Bool 
        '''
        if not self.gestor_cirujanos.hay_cirujanos_en_centro(receptor.centro):
            print(f"❌ No hay cirujanos disponibles en el centro de {receptor.nombre}")
            return False
        return True
