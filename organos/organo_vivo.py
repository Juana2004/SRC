
class OrganoVivo:

    
    def __init__(
        self, 
        nombre: str, 
        incucai
    ):
        self.nombre = nombre
        self.fecha_ablacion = None
        self.hora_ablacion = None
        incucai.registrar_organo(self)
