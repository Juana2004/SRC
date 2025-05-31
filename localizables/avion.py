from .vehiculos import Vehiculo
from .centro_de_salud import CentroDeSalud
from excepciones import ErrorGeolocalizacion



class Avion(Vehiculo):

    
    def __init__(self, nombre, velocidad, direccion, centro):
        super().__init__(nombre, velocidad, direccion, centro)

        try:
            if self.obtener_longlat():
                print(f"\n✔{self.nombre}.")
                self.incucai.registrar_avion(self)
        except ErrorGeolocalizacion as e:
            print(f" No se pudo registrar el avion: {e}")

    def puede_realizar_transporte(
        self, centro_origen: CentroDeSalud, centro_destino: CentroDeSalud
    ) -> bool:
        """
        Verifica si el vehiculo esta disponible para realizar el viaje
        Args:
            centro_origen: CentroDeSalud
            centro_destino: CentroDeSalud
        Returns:
            Bool
        """
        return (
            self.esta_disponible_para_ruta(centro_origen, centro_destino)
            and centro_origen.provincia != centro_destino.provincia
        )

    def ejecutar_transporte(
        self, centro_donante: CentroDeSalud, centro_receptor: CentroDeSalud
    ) -> float:
        """
        Ejecuta el transporte desde el centro donante hasta el centro del receptor.
        Actualiza la ubicacion del vehiculo en el transcurso del viaje e imprime su estado.
        Args:
            centro_donante: CentroDeSalud
            centro_receptor:CentroDeSalud
        Returns:
            Float
        """
        tiempo_total = self.calcular_tiempo_total_mision(
            centro_donante, centro_receptor
        )
        horas = int(tiempo_total)
        minutos = int(round((tiempo_total - horas) * 60))

        print(f"\nAVION asignado con éxito (velocidad: {self.velocidad} km/h)")

        print(f"🕒 Tiempo estimado del viaje: {horas}h {minutos}min.")

        print("\nYendo a recoger el órgano...")
        self.actualizar_ubicacion(centro_donante.longitud, centro_donante.latitud)

        print("\nTransportando órgano al centro de destino...")
        self.actualizar_ubicacion(centro_receptor.longitud, centro_receptor.latitud)

        return tiempo_total
