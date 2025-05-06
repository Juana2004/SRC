class Vehiculo:
    def __init__(self, velocidad, direccion, partido, provincia, pais, incucai):
        self.partido = partido
        self.provincia = provincia
        self.direccion = direccion
        self.pais = pais
        self.velocidad = velocidad
        self.registro_viajes = []

    def __str__(self):
        return f"{self.__class__.__name__}: Velocidad ={self.velocidad} km, viajes = {len(self.registro_viajes)}"
