from excepciones import ErrorGeolocalizacion
from geopy.geocoders import Nominatim
import time
from localizables.centro_de_salud import CentroDeSalud
import typing
from abc import ABC, abstractmethod


class Vehiculo(ABC):

    def __init__(
        self,
        nombre: str,
        velocidad: float,
        direccion: str,
        partido: str,
        provincia: str,
        pais: str,
        centro: CentroDeSalud,
        incucai,
    ):
        self.nombre = nombre
        self.partido = partido
        self.provincia = provincia
        self.direccion = direccion
        self.pais = pais
        self.velocidad = velocidad
        self.centro = centro
        self.geolocator = Nominatim(user_agent="incucai_app")
        self.viajes: int = 0
        if type(self) is Vehiculo:
            raise TypeError(
                "Vehiculo es una clase abstracta y no puede ser instanciada directamente."
            )

    def obtener_longlat(self) -> bool:
        self.full_address = (
            f"{self.direccion}, {self.partido}, {self.provincia}, {self.pais}"
        )
        self.location = self.obtener_ubicacion(self.full_address)
        if self.location:
            self.latitud = self.location.latitude
            self.longitud = self.location.longitude
            return True
        else:
            raise ErrorGeolocalizacion(self.full_address)

    def obtener_ubicacion(self, direccion: str, intentos_max=3, espera=2):
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

    def actualizar_ubicacion(self, longitud: float, latitud: float):
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

    def calcular_tiempo_hasta_origen(
        self, centro_donante: CentroDeSalud, calculador_distancias: callable
    ) -> float:
        distancia = calculador_distancias.obtener_distancia(self, centro_donante)
        return distancia / self.velocidad

    def calcular_tiempo_transporte(
        self,
        centro_donante: CentroDeSalud,
        centro_receptor: CentroDeSalud,
        calculador_distancias: callable,
    ) -> float:
        distancia = calculador_distancias.obtener_distancia(
            centro_donante, centro_receptor
        )
        return distancia / self.velocidad

    def esta_disponible_para_ruta(
        self, centro_origen: CentroDeSalud, centro_destino: CentroDeSalud
    ) -> bool:
        return self.centro in (centro_origen, centro_destino)

    def calcular_tiempo_total_mision(
        self,
        centro_donante: CentroDeSalud,
        centro_receptor: CentroDeSalud,
        calculador_distancias: callable,
    ) -> float:
        tiempo_recogida = self.calcular_tiempo_hasta_origen(
            centro_donante, calculador_distancias
        )
        tiempo_transporte = self.calcular_tiempo_transporte(
            centro_donante, centro_receptor, calculador_distancias
        )
        return tiempo_recogida + tiempo_transporte

    @abstractmethod
    def ejecutar_transporte(
        self,
        centro_donante: CentroDeSalud,
        centro_receptor: CentroDeSalud,
        calculador_distancias: callable,
    ):
        pass

    @abstractmethod
    def puede_realizar_transporte(
        self, centro_origen: CentroDeSalud, centro_destino: CentroDeSalud
    ):
        pass
