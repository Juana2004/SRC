from geopy.distance import distance
from localizables.centro_de_salud import CentroDeSalud



class CalculadorDistancias:

    
    def __init__(self):
        self._cache = {}

    def obtener_distancia(self, origen: object, destino: CentroDeSalud) -> float:
        """
        Calcula y retorna la distancia en kilómetros entre el origen y el destino,
        utilizando sus coordenadas geográficas. Usa una caché para evitar cálculos repetidos.
        Args:
            origen (object): Objeto con atributos 'latitud' y 'longitud'.
            destino (CentroDeSalud): Centro de salud con atributos 'nombre', 'latitud' y 'longitud'.
        Returns:
            float: Distancia en kilómetros entre el origen y el destino.
        """
        clave = (origen.nombre, destino.nombre)

        if clave not in self._cache:
            coords_origen = (origen.latitud, origen.longitud)
            coords_destino = (destino.latitud, destino.longitud)
            distancia_km = distance(coords_origen, coords_destino).km

            self._cache[clave] = distancia_km
            self._cache[(destino.nombre, origen.nombre)] = distancia_km

        return self._cache[clave]
