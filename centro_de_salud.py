from geopy.geocoders import Nominatim
import time

class CentroDeSalud:
    geolocator = Nominatim(user_agent="incucai_app")  # Clase compartida, evita múltiples instancias

    def __init__(self, nombre, direccion, partido, provincia, pais, incucai):
        self.nombre = nombre
        self.direccion = direccion
        self.partido = partido
        self.provincia = provincia
        self.pais = pais
        if self.obtener_longlat():
            print(f"\n✔ Centro de salud '{self.nombre}' registrado en: {self.full_address}")
            incucai.registrar_centro(self)
        else:
            print(f"No se pudo registrar el centro {self.nombre}, intente denuevo")

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
        """ Intenta obtener la geolocalización con reintentos en caso de error. """
        for intento in range(intentos_max):
            try:
                location = self.geolocator.geocode(direccion)
                if location:
                    return location
                else:
                    raise ValueError("Geolocalización fallida")
            except Exception as e:
                print(f"Error al obtener geolocalización: {e}. Intento {intento+1} de {intentos_max}")
                if intento < intentos_max - 1:
                    time.sleep(espera)  # Esperar antes de reintentar
        return None



