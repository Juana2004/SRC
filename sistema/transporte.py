from sistema.calculador_distancias import CalculadorDistancias
from localizables.vehiculos_terrestres import VehiculoTerrestre
class Transporte:
    def __init__(self, incucai):
        self.incucai = incucai
        self.calculador_distancias = CalculadorDistancias()
    
    def asignar_vehiculo(self, donante, receptor):
        """Asigna el mejor vehículo disponible para el transporte."""
        centro_donante = donante.centro
        centro_receptor = receptor.centro
        
        # Mostrar información básica
        distancia = self.calculador_distancias.obtener_distancia(centro_donante, centro_receptor)
        print(f"\n📍 Distancia entre centros: {distancia:.2f} km")
        
        # Determinar tipo de transporte y obtener vehículos
        vehiculos_candidatos = self._obtener_vehiculos_por_ubicacion(centro_donante, centro_receptor)
        
        if not vehiculos_candidatos:
            print("\n❌ No hay vehículos disponibles para esta ruta")
            return False, 0.0
        
        # Seleccionar el mejor vehículo
        mejor_vehiculo = self._seleccionar_mejor_vehiculo(vehiculos_candidatos, centro_donante, centro_receptor)
        
        # El vehículo ejecuta su propia misión
        tiempo_total = mejor_vehiculo.ejecutar_transporte(centro_donante, centro_receptor, self.calculador_distancias)
        
        return True, tiempo_total
    
    def _obtener_vehiculos_por_ubicacion(self, centro_origen, centro_destino):
        """Obtiene todos los vehículos que pueden realizar el transporte."""
        vehiculos_disponibles = []
        
        # Revisar aviones
        for avion in self.incucai.aviones:
            if avion.puede_realizar_transporte(centro_origen, centro_destino):
                vehiculos_disponibles.append(avion)
        
        # Revisar helicópteros
        for helicoptero in self.incucai.helicopteros:
            if helicoptero.puede_realizar_transporte(centro_origen, centro_destino):
                vehiculos_disponibles.append(helicoptero)
        
        # Revisar vehículos terrestres
        for vehiculo_terrestre in self.incucai.vehiculos_terrestres:
            if vehiculo_terrestre.puede_realizar_transporte(centro_origen, centro_destino):
                vehiculos_disponibles.append(vehiculo_terrestre)
        
        return vehiculos_disponibles
    
    def _seleccionar_mejor_vehiculo(self, vehiculos, centro_origen, centro_destino):
        """Selecciona el vehículo con menor tiempo total de misión."""
        def obtener_tiempo_estimado(vehiculo):
            if hasattr(vehiculo, 'calcular_tiempo_total_mision'):
                if isinstance(vehiculo, VehiculoTerrestre):  # VehiculoTerrestre
                    tiempo_total, _ = vehiculo.calcular_tiempo_total_mision(centro_origen, centro_destino, self.calculador_distancias)
                    return tiempo_total
                else:  # Avion o Helicoptero
                    return vehiculo.calcular_tiempo_total_mision(centro_origen, centro_destino, self.calculador_distancias)
            return float('inf')
        
        return min(vehiculos, key=obtener_tiempo_estimado)