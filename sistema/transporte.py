from sistema.calculador_distancias import CalculadorDistancias
from pacientes.paciente import Paciente
from pacientes.receptor import Receptor
from localizables.vehiculos import Vehiculo
from localizables.centro_de_salud import CentroDeSalud

class Transporte:
    def __init__(self, incucai):
        self.incucai = incucai
        self.calculador_distancias = CalculadorDistancias()


    def asignar_vehiculo(self, donante: Paciente, receptor: Receptor, vehiculos: list[Vehiculo]) -> tuple[bool, float]: 
        """
        Asigna un vehículo para transportar un órgano desde el centro de salud del donante al centro del receptor,
        informa la distancia entre centros, y ejecuta el transporte calculando el tiempo total.
        Args:
            donante: hereda de Paciente
            receptor: Receptor
            vehiculos: list[Vehiculo]: Lista de vehículos disponibles para el transporte.
        Returns:
            tuple:
                bool: Indica si la asignación y transporte se realizó con éxito (True)
                float: Tiempo total del transporte
         """
        centro_donante = donante.centro
        centro_receptor = receptor.centro
        self._informar_distancia(centro_donante, centro_receptor)

        vehiculo_optimo = self._seleccionar_mejor_vehiculo(vehiculos, centro_donante, centro_receptor)
        tiempo_total = vehiculo_optimo.ejecutar_transporte(centro_donante, centro_receptor, self.calculador_distancias)

        return True, tiempo_total

    def obtener_vehiculos_por_ubicacion(self, origen: CentroDeSalud, destino: CentroDeSalud) -> list[Vehiculo]:
        """
        Obtiene la lista de vehículos disponibles que pueden realizar un transporte entre dos centros de salud 
        Args:
            origen: CentroDeSalud
            destino: CentroDeSalud
        Returns:
            list[Vehiculo]
        """
        return [
            v for v in (self.incucai.aviones + self.incucai.helicopteros + self.incucai.vehiculos_terrestres)
            if v.puede_realizar_transporte(origen, destino)
        ]

    def _seleccionar_mejor_vehiculo(self, vehiculos: list[Vehiculo], origen: CentroDeSalud, destino: CentroDeSalud) -> Vehiculo:
        """
        Metodo privado
        Selecciona el vehículo que realiza el transporte entre origen y destino en el menor tiempo total 
        Args:
            vehiculos: list[Vehiculo]
            origen: CentroDeSalud
            destino: CentroDeSalud
        Returns:
            Vehiculo: El vehículo con el menor tiempo total  para el trayecto indicado.
            Si algún vehículo no tiene el método `calcular_tiempo_total_mision`, se le asigna un tiempo infinito para no seleccionarlo
        """
        return min(
            vehiculos,
            key=lambda v: v.calcular_tiempo_total_mision(origen, destino, self.calculador_distancias)
            if hasattr(v, 'calcular_tiempo_total_mision') else float('inf')
        )

    def _informar_distancia(self, origen: CentroDeSalud, destino: CentroDeSalud) -> float:
        """
        Metodo privado
        Calcula y muestra la distancia entre dos centros de salud
        Args:
            origen: CentroDeSalud
            destino: CentroDeSalud
        Returns:
            float: Distancia en km 
        """
        distancia = self.calculador_distancias.obtener_distancia(origen, destino)
        print(f"\n📍 Distancia entre centros: {distancia:.2f} km")
        return distancia
