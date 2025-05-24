from geopy.geocoders import Nominatim
from .vehiculos import Vehiculo
from excepciones import ErrorGeolocalizacion  
import random


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
        return (self.esta_disponible_para_ruta(centro_origen, centro_destino) and 
                centro_origen.provincia == centro_destino.provincia and
                centro_origen.partido == centro_destino.partido)
    
    def calcular_tiempo_total_mision(self, centro_donante, centro_receptor, calculador_distancias):
        #desde donde esta el vehiculo hasta centro donante
        tiempo_recogida = self.calcular_tiempo_hasta_origen(centro_donante, calculador_distancias)
        #desde centro donante hasta centro receptor
        tiempo_transporte = self.calcular_tiempo_transporte(centro_donante, centro_receptor, calculador_distancias)
        tiempo_trafico = random.randint(1, 30) / 60
        return tiempo_recogida + tiempo_transporte + tiempo_trafico, tiempo_trafico
    
    def ejecutar_transporte(self, centro_donante, centro_receptor, calculador_distancias):
        tiempo_total, tiempo_trafico = self.calcular_tiempo_total_mision(centro_donante, centro_receptor, calculador_distancias)
        horas = int(tiempo_total)
        minutos = int(round((tiempo_total - horas) * 60))
        horas_trafico = int(tiempo_trafico)
        minutos_trafico = int(round((tiempo_trafico - horas) * 60))

        print(f"\nVEHÍCULO TERRESTRE asignado con éxito (velocidad: {self.velocidad} km/h)")
        
        print(f"🕒 Tiempo estimado del viaje: {horas}h {minutos}min. Incluye {minutos_trafico}min de tráfico.")
        
        print("\nYendo a recoger el órgano...")
        self.actualizar_ubicacion(centro_donante.longitud, centro_donante.latitud)
        
        print("\nTransportando órgano al centro de destino...")
        self.actualizar_ubicacion(centro_receptor.longitud, centro_receptor.latitud)
        
        return tiempo_total

   