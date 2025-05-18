from geopy.geocoders import Nominatim
from localizables.vehiculos import Vehiculo
from localizables.excepciones import ErrorGeolocalizacion
import time

class Avion(Vehiculo):
    geolocator = Nominatim(user_agent="incucai_app")

    def __init__(self, nombre,velocidad, direccion, partido, provincia, pais, incucai):
        super().__init__(nombre,velocidad, direccion, partido, provincia, pais, incucai)

        self.full_address = f"{direccion}, {partido}, {provincia}, {pais}"
        try:
            location = self.obtener_ubicacion(self.full_address)
            if location:
                self.latitud = location.latitude
                self.longitud = location.longitude
                print(f"\n✔ Avión localizado correctamente en: {self.full_address}")
                incucai.registrar_avion(self)
            else:
                raise ErrorGeolocalizacion(self.full_address)
        except ErrorGeolocalizacion as e:
            print(f"❌ No se pudo registrar el avión: {e}")

    def obtener_ubicacion(self, direccion, intentos_max=3, espera=2):
        for intento in range(intentos_max):
            try:
                location = self.geolocator.geocode(direccion)
                if location:
                    return location
                else:
                    print(f"Geolocalización fallida")
            except Exception as e:
                print(f"⚠ Error al obtener geolocalización: {e}. Intento {intento+1} de {intentos_max}")
                if intento < intentos_max - 1:
                    time.sleep(espera)
                    
        raise ValueError(f"No se pudo geolocalizar la dirección: {direccion}")
