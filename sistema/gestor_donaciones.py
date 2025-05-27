from datetime import datetime
from typing import Tuple, Optional
from pacientes.donante_vivo import DonanteVivo
from sistema.gestor_cirujanos import GestorCirujanos
from sistema.compatibilidad import Compatibilidad
from .transporte import Transporte


class GestorDonaciones:

    def __init__(self, incucai):
        self.incucai = incucai
        self.gestor_cirujanos = GestorCirujanos(self)
        self.transporte = Transporte(incucai)

    def compatibilidad(self, receptor: object) -> list[Tuple[object, int]]:
        donantes = self.incucai.donantes
        organo_receptor = receptor.organo_receptor
        donantes_compatibles = []

        for donante in donantes:
            edad_compatible = Compatibilidad.edad_es_compatible(
                donante.edad, receptor.edad
            )
            sangre_compatible = Compatibilidad.sangre_es_compatible(donante, receptor)
            organo_compatible = Compatibilidad.organo_es_compatible(
                donante, organo_receptor
            )

            if sangre_compatible and edad_compatible and organo_compatible is not None:
                donantes_compatibles.append((donante, organo_compatible))

        return donantes_compatibles


    def procesar_donantes(
        self,
        donantes: list[object],
        receptor: object,
        receptores_pendientes: list[object],
    ) -> bool:
        for donante, indice_organo in donantes:
            if not self._cirujano_para_ablacion(donante):
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

    def _cirujano_para_ablacion(self, donante: object) -> bool: ##
        cirujanos = self.gestor_cirujanos.cirujanos_disponibles_ablacion(donante)
        if not cirujanos:
            print(f"⚠️ No hay cirujanos para ablación del donante {donante.nombre}")
            return False
        return True

    def _es_transporte_posible(self, donante: object, receptor: object) -> bool: ##
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

    def _realizar_ablacion(self, donante: object, receptor: object): ###
        print("🛠️ Iniciando proceso de ablación")
        cirujano = self.gestor_cirujanos.cirujanos_disponibles_ablacion(donante)[0]
        self.gestor_cirujanos.realizar_operacion_ablacion(cirujano, donante, receptor)

    def _gestionar_transporte( ##
        self, donante: object, receptor: object
    ) -> Optional[tuple[bool, float]]:
        if donante.centro == receptor.centro:
            print("🚑 Donante y receptor en el mismo centro")
            return True, 0.0
        exito, tiempo = self.transporte.asignar_vehiculo(donante, receptor)
        if not exito:
            print("❌ Transporte fallido. Match cancelado.")
        return exito, tiempo

    def _ejecutar_operacion( ##
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

    def _manejar_operacion_fallida( ##
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

    def _remover_si_sin_organos(self, donante: object): ##
        if not donante.organos_donante and donante in self.incucai.donantes:
            self.incucai.donantes.remove(donante)
            donante.centro.donantes.remove(donante)
            print(f"🗑️ Donante {donante.nombre} removido (sin órganos restantes)")

    def _reagendar_receptor(self, receptor: object, lista: list):
        if receptor in self.incucai.receptores:
            self.incucai.receptores.remove(receptor)
            lista.insert(0, receptor)
