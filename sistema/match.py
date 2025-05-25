from sistema.transporte import Transporte
from sistema.gestor_cirujanos import GestorCirujanos
from sistema.gestor_donaciones import GestorDonaciones
from typing import Optional


class Match:
    def __init__(self, incucai):
        self.incucai = incucai
        self.transporte = Transporte(incucai)
        self.gestor_cirujanos = GestorCirujanos(incucai)
        self.gestor_donaciones = GestorDonaciones(incucai)

    def match(self) -> bool:
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
                self._reportar_sin_donante(receptor)
                continue

            if self._procesar_donantes(
                donantes_compatibles, receptor, receptores_pendientes
            ):
                se_realizo_match = True
                receptores_procesados.add(id(receptor))
            else:
                print(f"\n❌ No se pudo realizar match para {receptor.nombre}\n")

        return se_realizo_match

    def _hay_cirujanos_en_centro(self, receptor: object) -> bool:
        if not self.gestor_cirujanos.hay_cirujanos_en_centro(receptor.centro):
            print(f"❌ No hay cirujanos disponibles en el centro de {receptor.nombre}")
            return False
        return True

    def _reportar_sin_donante(self, receptor: object):
        print(f"❌ No se encontró donante compatible para {receptor.nombre}")

    def _procesar_donantes(
        self,
        donantes: list[object],
        receptor: object,
        receptores_pendientes: list[object],
    ) -> bool:
        for donante, indice_organo in donantes:
            if not self._puede_realizar_ablacion(donante):
                continue

            if not self._es_transporte_posible(donante, receptor):
                continue

            print(f"✅ Match encontrado: {receptor.nombre} ↔ {donante.nombre}")
            self._realizar_ablacion(donante, receptor)

            exito_transporte, tiempo = self._gestionar_transporte(donante, receptor)
            if not exito_transporte:
                continue

            if self._ejecutar_operacion(donante, receptor, indice_organo, tiempo):
                return True

            self._manejar_operacion_fallida(
                donante, receptor, indice_organo, receptores_pendientes
            )

        return False

    def _puede_realizar_ablacion(self, donante: object) -> bool:
        cirujanos = self.gestor_cirujanos.cirujanos_disponibles_ablacion(donante)
        if not cirujanos:
            print(f"⚠️ No hay cirujanos para ablación del donante {donante.nombre}")
            return False
        return True

    def _es_transporte_posible(self, donante: object, receptor: object) -> bool:
        if donante.centro != receptor.centro:
            disponible = self.transporte.hay_vehiculos_disponibles(
                donante.centro, receptor.centro
            )
            if not disponible:
                print(
                    f"⚠️ Sin vehículos disponibles de {donante.centro.nombre} a {receptor.centro.nombre}"
                )
                return False
        return True

    def _realizar_ablacion(self, donante: object, receptor: object):
        print("🛠️ Iniciando proceso de ablación")
        cirujano = self.gestor_cirujanos.cirujanos_disponibles_ablacion(donante)[0]
        self.gestor_cirujanos.realizar_operacion_ablacion(cirujano)
        self.gestor_donaciones.registrar_ablacion_donante_vivo(
            donante, receptor.organo_receptor
        )

    def _gestionar_transporte(
        self, donante: object, receptor: object
    ) -> Optional[tuple[bool, float]]:
        if donante.centro == receptor.centro:
            print("🚑 Donante y receptor en el mismo centro")
            return True, 0.0
        exito, tiempo = self.transporte.asignar_vehiculo(donante, receptor)
        if not exito:
            print("❌ Transporte fallido. Match cancelado.")
        return exito, tiempo

    def _ejecutar_operacion(
        self, donante: object, receptor: object, indice_organo: int, tiempo: float
    ) -> bool:
        organo = donante.organos_donante[indice_organo]
        if self.gestor_cirujanos.evaluar_operacion(
            receptor.centro, organo, receptor, tiempo
        ):
            print("✅ Operación exitosa")
            self._realizar_trasplante(donante, receptor, indice_organo)
            return True
        return False

    def _manejar_operacion_fallida(
        self,
        donante: object,
        receptor: object,
        indice_organo: int,
        receptores_pendientes: list[object],
    ):
        if 0 <= indice_organo < len(donante.organos_donante):
            organo = donante.organos_donante.pop(indice_organo)
            print(f"❌ Órgano {organo.nombre} descartado tras operación fallida")
        self._remover_si_sin_organos(donante)
        self._reagendar_receptor(receptor, receptores_pendientes)

    def _realizar_trasplante(
        self, donante: object, receptor: object, indice_organo: int
    ):
        print(f"💉 Trasplante realizado: {donante.nombre} → {receptor.nombre}")
        self.incucai.receptores.remove(receptor)
        receptor.centro.receptores.remove(receptor)
        if 0 <= indice_organo < len(donante.organos_donante):
            donante.organos_donante.pop(indice_organo)
        self._remover_si_sin_organos(donante)

    def _remover_si_sin_organos(self, donante: object):
        if not donante.organos_donante and donante in self.incucai.donantes:
            self.incucai.donantes.remove(donante)
            donante.centro.donantes.remove(donante)
            print(f"🗑️ Donante {donante.nombre} removido (sin órganos restantes)")

    def _reagendar_receptor(self, receptor: object, lista: list):
        if receptor in self.incucai.receptores:
            self.incucai.receptores.remove(receptor)
            lista.insert(0, receptor)
