from excepciones import ErrorGeolocalizacion
from geopy.geocoders import Nominatim
from localizables.centro_de_salud import CentroDeSalud
from abc import ABC, abstractmethod
from localizables.geolocalizacion  import ServicioGeolocalizacion
from clases_type.direccion import Direccion


class Vehiculo(ABC):

    def __init__(
        self,
        nombre: str,
        velocidad: float,
        direccion: Direccion,
        centro: CentroDeSalud,
        incucai,
    ):
        if type(self) is Vehiculo:
            raise TypeError("Vehiculo es una clase abstracta y no puede ser instanciada directamente.")

        self.nombre = nombre
        self.velocidad = velocidad
        self.direccion: Direccion = direccion
        self.centro = centro
        self.geolocator = Nominatim(user_agent="incucai_app")
        self.viajes: int = 0
        self.servicio_geo = ServicioGeolocalizacion(self.geolocator)

    @abstractmethod
    def ejecutar_transporte(self,centro_donante: CentroDeSalud,centro_receptor: CentroDeSalud,calculador_distancias: callable,):
        pass

    @abstractmethod
    def puede_realizar_transporte(self, centro_origen: CentroDeSalud, centro_destino: CentroDeSalud):
        pass

    def obtener_longlat(self) -> bool:
        '''
        Obtiene las coordenadas geograficas del centro de salud.
        Si ocurre un error, lanza una excepcion.
        Returns:
            Bool
        '''
        try:
            coordenadas = self.servicio_geo.obtener_coordenadas(
                self.direccion.direccion,
                self.direccion.partido,
                self.direccion.provincia,
                self.direccion.pais
            )
            self.latitud = coordenadas.latitud
            self.longitud = coordenadas.longitud
            return True
        except ErrorGeolocalizacion:
            raise

    def actualizar_ubicacion(self, longitud: float, latitud: float):
        '''
        Actualiza la ubicacion del vehiculo, (utilizando una libreria?).
        Incrementa el contador de viajes en cada tramo del viaje.
        Args:
            longitud: float
            latitud: float
        '''
        try:
            self.latitud = latitud
            self.longitud = longitud
            location = self.geolocator.reverse((latitud, longitud), language="es")
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

    def calcular_tiempo_hasta_origen(self, centro_donante: CentroDeSalud, calculador_distancias: callable) -> float:
        '''
        Calcula el timpo que tarda el vehiculo desde su posicion actual hasta el centro de salud del donante.
        Args:
            centro_donante: CentroDeSalud

        Returns:
            Float
        '''
        distancia = calculador_distancias.obtener_distancia(self, centro_donante)
        return distancia / self.velocidad

    def calcular_tiempo_transporte(self, centro_donante: CentroDeSalud, centro_receptor: CentroDeSalud,calculador_distancias: callable,) -> float:
        '''
        Calcula el tiempo que tarda el vehiculo en realizar el trasporte desde el centro de salud del donante hasta el 
        centro de salud del receptor.
        Args:
            centro_donante: CentroDeSalud
            centro_receptor: CentroDeSalud
        Returns:
            Float
        '''
        distancia = calculador_distancias.obtener_distancia(centro_donante, centro_receptor)
        return distancia / self.velocidad

    def esta_disponible_para_ruta(self, centro_origen: CentroDeSalud, centro_destino: CentroDeSalud) -> bool:
        '''
        Verifica si el vehiculo esta disponible.
        Args:
            centro_origen: CentroDeSalud
            centro_destino: CentroDeSalud
        Returns:
            Bool
        '''
        return self.centro in (centro_origen, centro_destino)

    def calcular_tiempo_total_mision(self,centro_donante: CentroDeSalud,centro_receptor: CentroDeSalud,calculador_distancias: callable,) -> float:
        '''
        Calcula el tiempo que tardara el vehiculo en realizar todo el transporte, desde su ubicacion actual hasta el centro del receptor.
        Args:
            centro_donante: CentroDeSalud
            centro_receptor:CentroDeSalud
        Returns:
            float
        '''
        tiempo_recogida = self.calcular_tiempo_hasta_origen(
            centro_donante, calculador_distancias
        )
        tiempo_transporte = self.calcular_tiempo_transporte(
            centro_donante, centro_receptor, calculador_distancias
        )
        return tiempo_recogida + tiempo_transporte

