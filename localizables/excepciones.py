class ErrorGeolocalizacion(Exception):
    """Excepción lanzada cuando falla la geolocalización."""
    def __init__(self, direccion, mensaje="No se pudo geolocalizar la dirección"):
        self.direccion = direccion
        self.mensaje = f"{mensaje}: {direccion}"
        super().__init__(self.mensaje)


######seguir creando aca
