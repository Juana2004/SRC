class Organo:


    def __init__(self, nombre: str, fecha_ablacion, hora_ablacion, incucai):
        self.nombre = nombre
        self.fecha_ablacion = fecha_ablacion
        self.hora_ablacion = hora_ablacion
        incucai.registrar_organo(self)
