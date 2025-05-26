from geopy.geocoders import Nominatim
import time
from excepciones import ErrorGeolocalizacion, ErrorTipoDatoInvalido




class CentroDeSalud:

    
    geolocator = Nominatim(user_agent="incucai_app")

    def __init__(
        self, 
        nombre: str, 
        direccion: str, 
        partido: str, 
        provincia: str, 
        pais: str, 
        incucai
    ):
        self.nombre = nombre
        self.direccion = direccion
        self.partido = partido
        self.provincia = provincia
        self.pais = pais
        self.receptores: list[object] = []
        self.donantes: list[object] = []
        self.vehiculos: list[object] = []
        self.cirujanos: list[object] = []

        try:
            if self.obtener_longlat():
                print(f"\n✔'{self.nombre}' registrado en: {self.full_address}")
                incucai.registrar_centro(self)
        except (ErrorGeolocalizacion, ErrorTipoDatoInvalido) as e:
            print(f"❌ No se pudo registrar el centro '{self.nombre}': {e}")

    def __eq__(self, other):
        if isinstance(other, CentroDeSalud):
            return self.nombre == other.nombre and self.direccion == other.direccion
        return False

    def __hash__(self):
        return hash((self.nombre, self.direccion))

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
                    print(f"Geolocalización fallida")
            except Exception as e:

                print(
                    f"⚠ Error al obtener geolocalización: {e}. Intento {intento+1} de {intentos_max}"
                )

            if intento < intentos_max - 1:
                time.sleep(espera)

        raise ValueError(f"No se pudo geolocalizar la dirección: {direccion}")
