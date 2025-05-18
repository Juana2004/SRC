class Organoo:
    def __init__(self, nombre, incucai):
        self.nombre = nombre.lower()
        self.ablacion = None
        incucai.registrar_organo(self)