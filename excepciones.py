from enum import Enum
class ErrorGeolocalizacion(Exception):
    """Excepción lanzada cuando falla la geolocalización."""
    def __init__(self, direccion, mensaje="No se pudo geolocalizar la dirección"):
        self.direccion = direccion
        self.mensaje = f"{mensaje}: {direccion}"
        super().__init__(self.mensaje)

class ErrorDNIRepetido(Exception):
    """Excepción lanzada cuando un DNI ya está registrado en el sistema."""
    def __init__(self, nombre):
        self.mensaje = f"❌ El DNI de {nombre} ya está registrado en el sistema, no se registrara."
        super().__init__(self.mensaje)

class ErrorCentroNoRegistrado(Exception):
    """Excepción lanzada cuando el centro de salud no está registrado en el sistema."""
    def __init__(self, nombre_receptor, centro):
        self.mensaje = f"❌ Centro de salud '{centro}' de {nombre_receptor} no está registrado en el sistema, no se registrara."
        super().__init__(self.mensaje)

class ErrorCedulaRepetido(Exception):
    def __init__(self, nombre):
        self.mensaje = f"❌ La cedula de {nombre} ya está registrado en el sistema, no se registrara."
        super().__init__(self.mensaje)

class ErrorTipoDatoInvalido(Exception):
    def __init__(self, nombre, campo, tipo_esperado):
        super().__init__(f"El campo '{campo}' debe ser de tipo {tipo_esperado}, no se registrara {nombre}.")


######seguir creando aca
