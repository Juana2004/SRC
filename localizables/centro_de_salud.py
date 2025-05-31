from geopy.geocoders import Nominatim
from clases_type.direccion import Direccion
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
        self.incucai = incucai

        try:
            if self.obtener_longlat():
                print(f"\n✔'{self.nombre}' registrado.")
                self.incucai.registrar_centro(self)
        except (ErrorGeolocalizacion, ErrorTipoDatoInvalido) as e:
            print(f"No se registrara el centro de salud: {e}")

    def __eq__(self, other) -> bool:
        """
        Utilizando un metodo magico comparo si dos centros de salud tiene el mismo nombre y direccion.
        Args:
            other: CentroDeSalud
        Returns:
            Bool
        """
        if isinstance(other, CentroDeSalud):
            return self.nombre == other.nombre and self.direccion == other.direccion
        return False

    def __hash__(self) -> int:
        """
        devuelve un número entero que representa de manera única
        a un objeto, Python primero compara los hashes para ver si puede evitar usar __eq__ que es menos eficiente.
        """
        return hash((self.nombre, self.direccion))

    def obtener_longlat(self) -> bool:
        """
        Obtiene las coordenadas geograficas del centro de salud.
        Si ocurre un error, lanza una excepcion.
        Returns:
            Bool
        """
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
