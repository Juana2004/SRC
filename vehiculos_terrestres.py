from geopy.geocoders import Nominatim
from vehiculos import Vehiculo
import time


class VehiculoTerrestre(Vehiculo):
    geolocator = Nominatim(user_agent="incucai_app")

    def __init__(self, velocidad, direccion, partido, provincia, pais, incucai):
        super().__init__(velocidad, direccion, partido, provincia, pais, incucai)

        if self.obtener_longlat():
            print(f"\n✔ Vehículo terrestre localizado correctamente en: {self.full_address}")
            incucai.registrar_vehiculo_terr(self)
        else:
            print("No se pudo registrar el vehiculo , intente denuevo")
    
        
    def obtener_longlat(self):
        # Obtener latitud y longitud con manejo de excepciones
        self.full_address = f"{self.direccion}, {self.partido}, {self.provincia}, {self.pais}"
        location = self.obtener_ubicacion(self.full_address)
        if location:
            self.latitud = location.latitude
            self.longitud = location.longitude
            return True
        else:
            raise ValueError(f"No se pudo geolocalizar la dirección: {self.full_address}")
        
    
    def obtener_ubicacion(self, direccion, intentos_max=3, espera=2):
        for intento in range(intentos_max):
            try:
                location = self.geolocator.geocode(direccion)
                if location:
                    return location
                else:
                    raise ValueError("Geolocalización fallida")
            except Exception as e:
                print(f"⚠ Error al obtener geolocalización: {e}. Intento {intento+1} de {intentos_max}")
                if intento < intentos_max - 1:
                    time.sleep(espera)
        return None
    
    def actualizar_ubicacion(self, longitud, latitud):
            geolocator = Nominatim(user_agent="mi_aplicacion")
            self.latitud = latitud
            self.longitud = longitud
            location = geolocator.reverse((latitud, longitud), language='es')
            print(f"\n✔ Ubicación actualizada a: {location}")