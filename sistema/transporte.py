from sistema.calculador_distancias import CalculadorDistancias

class Transporte:
    def __init__(self, incucai):
        self.incucai = incucai
        self.calculador_distancias = CalculadorDistancias()

    def hay_vehiculos_disponibles(self, centro_donante, centro_receptor) -> bool:
        return bool(self._obtener_vehiculos_por_ubicacion(centro_donante, centro_receptor))

    def asignar_vehiculo(self, donante, receptor):
        centro_donante = donante.centro
        centro_receptor = receptor.centro

        self._informar_distancia(centro_donante, centro_receptor)
        vehiculos = self._obtener_vehiculos_por_ubicacion(centro_donante, centro_receptor)

        if not vehiculos:
            self._informar_ausencia_vehiculos()
            return False, 0.0

        vehiculo_optimo = self._seleccionar_mejor_vehiculo(vehiculos, centro_donante, centro_receptor)
        tiempo_total = vehiculo_optimo.ejecutar_transporte(centro_donante, centro_receptor, self.calculador_distancias)

        return True, tiempo_total

    def _obtener_vehiculos_por_ubicacion(self, origen, destino):
        return [
            v for v in (self.incucai.aviones + self.incucai.helicopteros + self.incucai.vehiculos_terrestres)
            if v.puede_realizar_transporte(origen, destino)
        ]

    def _seleccionar_mejor_vehiculo(self, vehiculos, origen, destino):
        return min(
            vehiculos,
            key=lambda v: v.calcular_tiempo_total_mision(origen, destino, self.calculador_distancias)
            if hasattr(v, 'calcular_tiempo_total_mision') else float('inf')
        )

    def _informar_distancia(self, origen, destino):
        distancia = self.calculador_distancias.obtener_distancia(origen, destino)
        print(f"\n📍 Distancia entre centros: {distancia:.2f} km")
        return distancia

    def _informar_ausencia_vehiculos(self):
        print("\n❌ No hay vehículos disponibles para esta ruta")
