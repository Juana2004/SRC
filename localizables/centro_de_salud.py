from geopy.geocoders import Nominatim
from .direccion import Direccion
from excepciones import ErrorGeolocalizacion, ErrorTipoDatoInvalido
from .geolocalizacion import ServicioGeolocalizacion


class CentroDeSalud:

    def __init__(
        self,
        nombre: str,
        direccion: Direccion,
        incucai,
    ):
        self.nombre = nombre
        self.direccion: Direccion = direccion
        self.partido: str = direccion.partido
        self.provincia: str = direccion.provincia
        self.pais: str = direccion.pais
        self.receptores: list[object] = []
        self.donantes: list[object] = []
        self.vehiculos: list[object] = []
        self.cirujanos: list[object] = []
        self.geolocator = Nominatim(user_agent="incucai_app")
        self.servicio_geo = ServicioGeolocalizacion(self.geolocator)

        try:
            if self.obtener_longlat():
                print(f"\n✔'{self.nombre}' registrado.")
                incucai.registrar_centro(self)
        except (ErrorGeolocalizacion, ErrorTipoDatoInvalido) as e:
            print(e)

    def __eq__(self, other):
        if isinstance(other, CentroDeSalud):
            return self.nombre == other.nombre and self.direccion == other.direccion
        return False

    def __hash__(self):
        return hash((self.nombre, self.direccion))

    def obtener_longlat(self) -> bool:
        try:
            coordenadas = self.servicio_geo.obtener_coordenadas(
                self.direccion.direccion,
                self.direccion.partido,
                self.direccion.provincia,
                self.direccion.pais,
            )
            self.latitud = coordenadas.latitud
            self.longitud = coordenadas.longitud
            return True
        except ErrorGeolocalizacion:
            raise
