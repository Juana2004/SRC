class Organo:
    def __init__(self, nombre, ablacion, incucai):
        self.nombre = nombre.lower()
        self.ablacion = ablacion
        incucai.registrar_organo(self)
