from .vehiculos import Vehiculo
from .centro_de_salud import CentroDeSalud
from excepciones import ErrorGeolocalizacion
import random



class VehiculoTerrestre(Vehiculo):
    def __init__(self, nombre, velocidad, direccion, centro, incucai):
        super().__init__(nombre, velocidad, direccion, centro, incucai)

        try:
            if self.obtener_longlat():
                print(
                    f"\n✔{self.nombre} "
                )
                incucai.registrar_vehiculo_terrestre(self)
        except ErrorGeolocalizacion as e:
            print(f" No se pudo registrar el vehículo terrestre: {e}")

    def puede_realizar_transporte(self, centro_origen: CentroDeSalud, centro_destino: CentroDeSalud) -> bool:
        '''
        Verifica si el vehiculo esta disponible para realizar el viaje
        Args:
            centro_origen: CentroDeSalud
            centro_destino: CentroDeSalud
        Returns:
            Bool
        '''
        return (
            self.esta_disponible_para_ruta(centro_origen, centro_destino)
            and centro_origen.provincia == centro_destino.provincia
            and centro_origen.partido == centro_destino.partido
        )

    def ejecutar_transporte(self,centro_donante: CentroDeSalud,centro_receptor: CentroDeSalud) -> float:
        '''
        Ejecuta el transporte desde el centro donante hasta el centro del receptor.
        Actualiza la ubicacion del vehiculo en el transcurso del viaje e imprime su estado.
        Args:
            centro_donante: CentroDeSalud
            centro_receptor:CentroDeSalud
        Returns:
            Float
        '''
        tiempo_recorrido = self.calcular_tiempo_total_mision(
            centro_donante, centro_receptor
        )
        tiempo_trafico = random.randint(1, 30) / 60
        tiempo_total = tiempo_recorrido + tiempo_trafico
        horas = int(tiempo_total)
        minutos = int(round((tiempo_total - horas) * 60))
        horas_trafico = int(tiempo_trafico)
        minutos_trafico = int(round((tiempo_trafico - horas) * 60))

        print(
            f"\nVEHÍCULO TERRESTRE asignado con éxito (velocidad: {self.velocidad} km/h)"
        )

        print(
            f"🕒 Tiempo estimado del viaje: {horas}h {minutos}min. Incluye {horas_trafico}h {minutos_trafico}min de tráfico."
        )

        print("\nYendo a recoger el órgano...")
        self.actualizar_ubicacion(centro_donante.longitud, centro_donante.latitud)

        print("\nTransportando órgano al centro de destino...")
        self.actualizar_ubicacion(centro_receptor.longitud, centro_receptor.latitud)

        return tiempo_total
