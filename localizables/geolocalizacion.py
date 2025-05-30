import time
from dataclasses import dataclass
from typing import Optional, Any
from excepciones import ErrorGeolocalizacion
from clases_type.coordenadas import Coordenadas


class ServicioGeolocalizacion:
    def __init__(self, geolocator):
        self.geolocator = geolocator

    def obtener_coordenadas(self, direccion: str, partido: str, provincia: str, pais: str) -> Coordenadas:
        '''
        Obtiene las coordenadas geograficas a partir de una direccion.
        Si no se puedeobtener la ubicacion, lanza una excepcion.
        Args:
            direccion: str
            partido:str
            provincia:str
            pais: str
        Returns:
            Coordenadas:
        '''
        full_address = f"{direccion}, {partido}, {provincia}, {pais}"
        location = self._obtener_ubicacion(full_address)

        if location:
            return Coordenadas(latitud=location.latitude, longitud=location.longitude)
        else:
            raise ErrorGeolocalizacion(full_address)

    def _obtener_ubicacion(self, direccion: str, intentos_max: int = 3, espera: int = 2) -> Optional[object]:
        '''
        "Intenta" obtener una ubicación geográfica a partir de una dirección de texto.
        Reintenta hasta 3 veces, con una espera de 2 segundos entre intentos.
        Imprime el error correspondiente en cada intento fallido.
        Args:
            direccion: str
            intentos_max: int 
            espera: int 
        Returns:
            Objeto de ubicación si se encuentra
            None si todos los intentos fallan
        '''
        for intento in range(intentos_max):
            try:
                location = self.geolocator.geocode(direccion)
                if location:
                    return location
                else:
                    raise ValueError("Direccion ingresada no reconocida")
            except Exception as e:
                print(
                    f"⚠ Error encontrando ubicacion. Intento {intento+1} de {intentos_max}"
                )
                if intento < intentos_max - 1:
                    time.sleep(espera)
        return None
