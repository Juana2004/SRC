import random
from geopy.distance import distance

class Transporte:
    """Gestor de transporte de órganos"""
    
    def __init__(self, incucai):
        self.incucai = incucai
        self._distancias_cache = {}
    
    def calcular_distancia(self, centro1, centro2) -> float:
        """Calcula la distancia entre dos centros de salud o vehiculo con centro"""
        clave = (centro1.nombre, centro2.nombre)
        if clave not in self._distancias_cache:
            coords_1 = (centro1.latitud, centro1.longitud)
            coords_2 = (centro2.latitud, centro2.longitud)
            self._distancias_cache[clave] = distance(coords_1, coords_2).km
            self._distancias_cache[(centro2.nombre, centro1.nombre)] = self._distancias_cache[clave]
        return self._distancias_cache[clave]
        
    def asignar_vehiculo(self, donante, receptor) -> bool:
        """Determina y asigna el vehículo apropiado según la distancia y disponibilidad"""
        centro_donante = donante.centro
        centro_receptor = receptor.centro
        distancia = self.calcular_distancia(centro_donante, centro_receptor)
        
        print(f"\n📍 Distancia entre centros: {distancia:.2f} km")
        
        # Selección de transporte según ubicación
        if centro_donante.provincia != centro_receptor.provincia:
            return self._asignar_aereo("AVIÓN", self.incucai.aviones)
            
        elif centro_donante.partido != centro_receptor.partido:
            return self._asignar_aereo("HELICÓPTERO", self.incucai.helic)
            
        else:
            return self._asignar_terrestre(donante, centro_receptor)
    
    def _asignar_aereo(self, tipo, vehiculos) -> bool:
        print(f"\n✈️ Transporte requerido: {tipo}")
        if vehiculos:
            print(f"\n{tipo} asignado con éxito.")
            return True
        else:
            print(f"\n❌ No hay {tipo.lower()}s disponibles.")
            return False
            
    def _asignar_terrestre(self, donante, centro_destino) -> bool:
        """Asigna el vehículo terrestre según velocidad, distancia y trafico"""
        print("\n🚑 Transporte requerido: VEHÍCULO TERRESTRE")
        vehiculos = self.incucai.vehiculos_terr
        
        if not vehiculos:
            print("\n❌ No hay vehículos terrestres disponibles.")
            return False
            
        # Ordenar vehículos 
        vehiculos_ordenados = sorted(
            vehiculos,
            key=lambda v: (
                self.calcular_distancia(v, donante.centro) / v.velocidad + random.randint(0, 60) / 60
            )
        )
        
        vehiculo = vehiculos_ordenados[0]
        print(f"\nVehículo terrestre asignado con éxito (velocidad: {vehiculo.velocidad})")
        
        # Simular ruta del vehículo
        print("\nYendo a recoger el órgano...")
        vehiculo.actualizar_ubicacion(donante.centro.longitud, donante.centro.latitud)
        print("\nTransportando órgano al centro de destino...")
        vehiculo.actualizar_ubicacion(centro_destino.longitud, centro_destino.latitud)
        return True