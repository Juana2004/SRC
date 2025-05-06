from geopy.geocoders import Nominatim
from vehiculos import Vehiculo
import time

class Helicoptero(Vehiculo):
    geolocator = Nominatim(user_agent="incucai_app")

    def __init__(self, velocidad, direccion, partido, provincia, pais, incucai):
        super().__init__(velocidad, direccion, partido, provincia, pais, incucai)
        full_address = f"{direccion}, {partido}, {provincia}, {pais}"
        location = self.obtener_ubicacion(full_address)
        if location:
            self.latitud = location.latitude
            self.longitud = location.longitude
            print(f"\n✔ Helicóptero localizado correctamente en: {full_address}")
        else:
            raise ValueError(f"\n✘ No se pudo geolocalizar la dirección: {full_address}")
        incucai.registrar_helic(self)

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
