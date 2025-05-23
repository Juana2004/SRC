from excepciones import ErrorGeolocalizacion
from geopy.geocoders import Nominatim
import time
class Vehiculo:


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
        self.nombre = nombre
        self.partido = partido
        self.provincia = provincia
        self.direccion = direccion
        self.pais = pais
        self.velocidad: int = velocidad
        self.centro: object = centro

    def obtener_longlat(self):
        self.full_address = (
            f"{self.direccion}, {self.partido}, {self.provincia}, {self.pais}"
        )
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
                print(
                    f"⚠ Error al obtener geolocalización: {e}. Intento {intento+1} de {intentos_max}"
                )
                if intento < intentos_max - 1:
                    time.sleep(espera)
        return None

    def actualizar_ubicacion(self, longitud, latitud):
        try:
            geolocator = Nominatim(user_agent="incucai_app")
            self.latitud = latitud
            self.longitud = longitud
            location = geolocator.reverse((latitud, longitud), language="es")
            if location:
                self.viajes += 1
                print(f"\n✔ Ubicación actualizada a: {location}")
                print(f"Viajes del vehiculo: {self.viajes}")
            else:
                raise ErrorGeolocalizacion(
                    f"Coordenadas: {latitud}, {longitud}",
                    mensaje="No se pudo invertir la geolocalización",
                )
        except Exception as e:
            print(f"❌ Error al actualizar ubicación: {e}")

    def calcular_tiempo_hasta_origen(self, centro_origen, calculador_distancias):
        """Calcula el tiempo necesario para llegar al punto de recogida."""
        from geopy.distance import distance
        coords_vehiculo = (self.latitud, self.longitud)
        coords_origen = (centro_origen.latitud, centro_origen.longitud)
        distancia = distance(coords_vehiculo, coords_origen).km
        return distancia / self.velocidad
    
    def calcular_tiempo_transporte(self, centro_origen, centro_destino):
        """Calcula el tiempo de transporte entre origen y destino."""
        from geopy.distance import distance
        coords_origen = (centro_origen.latitud, centro_origen.longitud)
        coords_destino = (centro_destino.latitud, centro_destino.longitud)
        distancia = distance(coords_origen, coords_destino).km
        return distancia / self.velocidad
    
    def esta_disponible_para_ruta(self, centro_origen, centro_destino):
        """Determina si el vehículo está disponible para realizar el transporte."""
        return self.centro in (centro_origen, centro_destino)

