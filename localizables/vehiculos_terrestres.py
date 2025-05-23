from geopy.geocoders import Nominatim
from .vehiculos import Vehiculo
from excepciones import ErrorGeolocalizacion  


class VehiculoTerrestre(Vehiculo):
    geolocator = Nominatim(user_agent="incucai_app")

    def __init__(
        self,
        nombre: str,
        velocidad: float,
        direccion: str,
        partido: str,
        provincia: str,
        pais: str,
        centro: object,
        incucai,
    ):
        super().__init__(
            nombre, velocidad, direccion, partido, provincia, pais, centro, incucai
        )
        self.viajes = 0

        try:
            if self.obtener_longlat():
                print(
                    f"\n✔{self.nombre} localizado correctamente en: {self.full_address}"
                )
                incucai.registrar_vehiculo_terrestre(self)
        except ErrorGeolocalizacion as e:
            print(f"❌ No se pudo registrar el vehículo terrestre: {e}")

    
    def puede_realizar_transporte(self, centro_origen, centro_destino):
        """Los vehículos terrestres operan dentro del mismo partido."""
        return (self.esta_disponible_para_ruta(centro_origen, centro_destino) and 
                centro_origen.provincia == centro_destino.provincia and
                centro_origen.partido == centro_destino.partido)
    
    def calcular_tiempo_total_mision(self, centro_origen, centro_destino, calculador_distancias):
        """Calcula el tiempo total incluyendo tráfico."""
        import random
        tiempo_recogida = self.calcular_tiempo_hasta_origen(centro_origen, calculador_distancias)
        tiempo_transporte = self.calcular_tiempo_transporte(centro_origen, centro_destino)
        tiempo_trafico = random.randint(0, 60) / 60
        return tiempo_recogida + tiempo_transporte + tiempo_trafico, tiempo_trafico
    
    def ejecutar_transporte(self, centro_origen, centro_destino, calculador_distancias):
        """Ejecuta la misión completa de transporte terrestre."""
        tiempo_total, tiempo_trafico = self.calcular_tiempo_total_mision(centro_origen, centro_destino, calculador_distancias)
        
        print(f"\nVEHÍCULO TERRESTRE asignado con éxito (velocidad: {self.velocidad} km/h)")
        print(f"⏱️ Tiempo estimado total: {tiempo_total:.2f} horas (incluye {tiempo_trafico:.2f}h de tráfico)")
        
        print("\nYendo a recoger el órgano...")
        self.actualizar_ubicacion(centro_origen.longitud, centro_origen.latitud)
        
        print("\nTransportando órgano al centro de destino...")
        self.actualizar_ubicacion(centro_destino.longitud, centro_destino.latitud)
        
        return tiempo_total

   