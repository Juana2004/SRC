class Vehiculo:
    def __init__(self, velocidad, direccion, partido, provincia):
        self.partido = partido
        self.provincia = provincia
        self.direccion = direccion
        self.velocidad = velocidad
        self.registro_viajes = []

    def __str__(self):
        return f"{self.__class__.__name__}: vel={self.velocidad}, viajes={len(self.registro_viajes)}"
