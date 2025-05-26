import time
from dataclasses import dataclass
from typing import Optional, Any
from excepciones import ErrorGeolocalizacion
from .coordenadas import Coordenadas


class ServicioGeolocalizacion:
    def __init__(self, geolocator):
        self.geolocator = geolocator

    def obtener_coordenadas(
        self, direccion: str, partido: str, provincia: str, pais: str
    ) -> Coordenadas:
        full_address = f"{direccion}, {partido}, {provincia}, {pais}"
        location = self._obtener_ubicacion(full_address)

        if location:
            return Coordenadas(latitud=location.latitude, longitud=location.longitude)
        else:
            raise ErrorGeolocalizacion(full_address)

    def _obtener_ubicacion(
        self, direccion: str, intentos_max: int = 3, espera: int = 2
    ) -> Optional[Any]:
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
