class Organo:
    def __init__(self, tipo, estado="estable", fecha_extraccion=None, compatibilidad=None):
        self.tipo = tipo.lower()
        self.estado = estado.lower()
        self.fecha_extraccion = fecha_extraccion
        self.compatibilidad = compatibilidad  # puede ser 'compatible' o 'no compatible'

    def esta_disponible(self):
        #Verifica si el órgano está disponible para el trasplante
        return self.estado == "estable" and self.compatibilidad == "compatible"

    def marcar_trasplantado(self):
        #Marca el órgano como trasplantado
        self.estado = "trasplantado"

    def __str__(self):
        return f"{self.tipo.capitalize()} - Estado: {self.estado}, Fecha de extracción: {self.fecha_extraccion}, Compatibilidad: {self.compatibilidad}"
