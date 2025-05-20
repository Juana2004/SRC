from geopy.geocoders import Nominatim
from localizables.vehiculos import Vehiculo
from excepciones import ErrorGeolocalizacion
import time

class Avion(Vehiculo):
    geolocator = Nominatim(user_agent="incucai_app")

    def __init__(self, nombre, velocidad, direccion, partido, provincia, pais, centro, incucai):
        super().__init__(nombre, velocidad, direccion, partido, provincia, pais, centro, incucai)
        self.viajes = 0
        
        try:
            if self.obtener_longlat():
                print(f"\n✔ {self.nombre} localizado correctamente en: {self.full_address}")
                incucai.registrar_avion(self)
        except ErrorGeolocalizacion as e:
            print(f"❌ No se pudo registrar el avion: {e}")

    def obtener_longlat(self):
        self.full_address = f"{self.direccion}, {self.partido}, {self.provincia}, {self.pais}"
        location = self.obtener_ubicacion(self.full_address)
        if location:
            self.latitud = location.latitude
            self.longitud = location.longitude
            return True
        else:
            raise ErrorGeolocalizacion(self.full_address)

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
        try:
            geolocator = Nominatim(user_agent="incucai_app")
            self.latitud = latitud
            self.longitud = longitud
            location = geolocator.reverse((latitud, longitud), language='es')
            if location:
                self.viajes += 1
                print(f"\n✔ Ubicación actualizada a: {location}")
                print(f"Viajes del vehiculo: {self.viajes}")
            else:
                raise ErrorGeolocalizacion(f"Coordenadas: {latitud}, {longitud}", mensaje="No se pudo invertir la geolocalización")
        except Exception as e:
            print(f"❌ Error al actualizar ubicación: {e}")
