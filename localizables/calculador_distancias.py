from geopy.distance import distance
from localizables.centro_de_salud import CentroDeSalud



class CalculadorDistancias:

    
    def __init__(self):
        self._cache = {}

    def obtener_distancia(self, origen: object, destino: CentroDeSalud) -> float:
        clave = (origen.nombre, destino.nombre)

        if clave not in self._cache:
            coords_origen = (origen.latitud, origen.longitud)
            coords_destino = (destino.latitud, destino.longitud)
            distancia_km = distance(coords_origen, coords_destino).km

            self._cache[clave] = distancia_km
            self._cache[(destino.nombre, origen.nombre)] = distancia_km

        return self._cache[clave]
