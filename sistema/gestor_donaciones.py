from typing import Tuple, Optional
from .gestor_cirujanos import GestorCirujanos
from .compatibilidad import Compatibilidad
from .transporte import Transporte
from pacientes.receptor import Receptor
from pacientes.paciente import Paciente
from localizables.vehiculos import Vehiculo


class GestorDonaciones:

    def __init__(self, incucai):
        self.incucai = incucai
        self.gestor_cirujanos = GestorCirujanos(self)
        self.transporte = Transporte(incucai)

    def compatibilidad(self, receptor: object) -> list[Tuple[Paciente, int]]:
        '''
        Para cada donante, verifica si la edad, el tipo de sangre y el órgano son compatibles
        con el receptor. Si todos los criterios son compatibles, agrega el donante a la lista
        junto con el indice del organo requerido en la lista de organos de este.
        Args:
            receptor: Receptor 
        Returns:
            list[Tuple[Paciente, int]]: Lista de tuplas 
        '''
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
        donantes: list[Paciente],
        receptor: object,
        receptores_pendientes: list[Receptor],
    ) -> bool:
        for donante, indice_organo in donantes:
            print(f"\nEvaluando donantes compatibles en sangre, organos y edad para {receptor.nombre}")
            print(f"Evaluando donante {donante.nombre}:")

            cirujanos = self.gestor_cirujanos.cirujanos_disponibles_ablacion(donante)
            if not cirujanos:
                print(f"⚠️ No hay cirujanos para realizar la ablación.")
                continue

            if donante.centro != receptor.centro:
                vehiculos = self.transporte.obtener_vehiculos_por_ubicacion(
                    donante.centro, receptor.centro
                )
                if not vehiculos:
                    print(
                        f"⚠️ Sin vehículos disponibles de {donante.centro.nombre} a {receptor.centro.nombre}"
                    )
                    continue

            print(f"\n✅ Match encontrado: {receptor.nombre} ↔ {donante.nombre}\n")
            print("\n Iniciando proceso de ablación\n")
            cirujano = cirujanos[0]
            self.gestor_cirujanos.realizar_operacion_ablacion(
                cirujano, donante, receptor
            )

            exito_transporte, tiempo = self._gestionar_transporte(
                donante, receptor, vehiculos
            )

            if self._ejecutar_operacion(donante, receptor, indice_organo, tiempo):
                return True

            self._manejar_operacion_fallida(
                donante, receptor, indice_organo, receptores_pendientes
            )

        return False

    def _gestionar_transporte(self, donante: Paciente, receptor: Receptor, vehiculos: list[Vehiculo]) -> Optional[tuple[bool, float]]:
        '''
        Metodo privado
        Verifica si el donante y el receptor estan en el mismo centro, en caso de no estarlo les asigna un vehiculo.
        Args:
            donante: hereda de clase Paciente
            receptor: Receptor
            vehiculos: lista de clase del tipo Vehiculo
        Returns:
            Tupla de bool y float -> float puede ser 0
        '''
        if donante.centro == receptor.centro:
            print("\n🚑 Donante y receptor en el mismo centro")
            return True, 0.0
        exito, tiempo = self.transporte.asignar_vehiculo(donante, receptor, vehiculos)
        return exito, tiempo

    def _ejecutar_operacion(self, donante: Paciente, receptor: Receptor, indice_organo: int, tiempo: float) -> bool:
        '''
        Metodo privado
        Ejecuta el metodo encargado de realizar la operacion, en caso de exito, lo informa e implementa el translado de organo.
        Args:
            donante: Paciente
            receptor: Receptor
            indice_organo: int
            tiempo: float
        returns:
            bool
        '''
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
        donante: Paciente,
        receptor: Receptor,
        indice_organo: int,
        receptores_pendientes: list[Receptor],
    ):
        '''
        Metodo privado
        Es implementado en caso de que la operacion falle, elimina el organo de la lista de organos del donante, 
        marca al receptor como "inestable" y reordena la lista de receptores, dejandolo primero.
        Args:
            donante: Paciente
            receptor: Receptor
            indice_organo: int
            receptores_pendientes: lista de Receptor
        '''
        if 0 <= indice_organo < len(donante.organos_donante):
            organo = donante.organos_donante.pop(indice_organo)
            print(f"❌ Órgano {organo.nombre} descartado tras operación fallida")
        self._remover_si_sin_organos(donante)
        receptor.estado = "inestable"
        self.incucai.receptores.sort()



    def _realizar_trasplante(
        self, donante: Paciente, receptor: Receptor, indice_organo: int
    ):
        '''
        Metodo privado
        Es implementado en caso de operacion exitosa, elimina el receptor de la lista de espera y de su centro. Elimina el organo de la
        lista de organos del donante e implementa un metodo.
        Args:
            donante: Paciente
            receptor: Receptor
            indice_organo: int
        '''
        print(f"💉 Trasplante realizado: {donante.nombre} → {receptor.nombre}")
        self.incucai.receptores.remove(receptor)
        receptor.centro.receptores.remove(receptor)
        if 0 <= indice_organo < len(donante.organos_donante):
            donante.organos_donante.pop(indice_organo)
        self._remover_si_sin_organos(donante)

    def _remover_si_sin_organos(self, donante: Paciente):  
        '''
        Se encarga de eliminar un donante si ya no tiene mas organos para donar y lo informa.
        Args:
            donante: Paciente
        '''
        if not donante.organos_donante and donante in self.incucai.donantes:
            self.incucai.donantes.remove(donante)
            donante.centro.donantes.remove(donante)
            print(f"\n Donante {donante.nombre} removido (sin órganos restantes)\n")

