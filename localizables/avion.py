from geopy.geocoders import Nominatim
from .vehiculos import Vehiculo
from excepciones import ErrorGeolocalizacion, ErrorCentroNoRegistrado, ErrorTipoDatoInvalido


class Avion(Vehiculo):
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
        incucai
    ):
        super().__init__(
            nombre, velocidad, direccion, partido, provincia, pais, centro, incucai
        )
        self.viajes = 0

        try:
            if self.obtener_longlat():
                print(
                    f"\n✔ {self.nombre} localizado correctamente en: {self.full_address}"
                )
                incucai.registrar_avion(self)
        except ErrorGeolocalizacion as e:
            print(f"❌ No se pudo registrar el avion: {e}")

    def puede_realizar_transporte(self, centro_origen, centro_destino):
        """Los aviones solo operan entre diferentes provincias."""
        return (self.esta_disponible_para_ruta(centro_origen, centro_destino) and 
                centro_origen.provincia != centro_destino.provincia)
    
    def calcular_tiempo_total_mision(self, centro_origen, centro_destino, calculador_distancias):
        """Calcula el tiempo total de la misión aérea."""
        tiempo_recogida = self.calcular_tiempo_hasta_origen(centro_origen, calculador_distancias)
        tiempo_transporte = self.calcular_tiempo_transporte(centro_origen, centro_destino)
        return tiempo_recogida + tiempo_transporte
    
    def ejecutar_transporte(self, centro_origen, centro_destino, calculador_distancias):
        """Ejecuta la misión completa de transporte en avión."""
        tiempo_total = self.calcular_tiempo_total_mision(centro_origen, centro_destino, calculador_distancias)
        
        print(f"\nAVIÓN asignado con éxito (velocidad: {self.velocidad} km/h)")
        print(f"⏱️ Tiempo estimado total: {tiempo_total:.0f} horas")
        
        print("\nYendo a recoger el órgano...")
        self.actualizar_ubicacion(centro_origen.longitud, centro_origen.latitud)
        
        print("\nTransportando órgano al centro de destino...")
        self.actualizar_ubicacion(centro_destino.longitud, centro_destino.latitud)
        
        return tiempo_total