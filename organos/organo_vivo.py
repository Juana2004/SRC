from datetime import datetime

class OrganoVivo:

    
    def __init__(
        self, 
        nombre: str, 
        incucai
    ):
        self.nombre = nombre.lower()
        self.ablacion: datetime = None
        incucai.registrar_organo(self)
