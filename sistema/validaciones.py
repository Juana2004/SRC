from excepciones import *

class Validaciones:
    def __init__(self, incucai):
        self.incucai = incucai
    def validar_centro_registrado(self, persona: object):
            if persona.centro not in self.incucai.centros_salud:
                raise ErrorCentroNoRegistrado(persona.nombre, persona.centro)

    def validar_dni_unico(self, persona: object):
        if persona in self.incucai.donantes + self.incucai.receptores:
            raise ErrorDNIRepetido(persona.nombre)
        
    def validar_dni_unico_por_int(self, dni: int):
        """
        Verifica si el DNI ya está registrado entre donantes o receptores.
        Lanza ErrorDNIRepetido si encuentra duplicado.
        """
        for persona in self.incucai.donantes + self.incucai.receptores:
            if persona.datos.dni == dni:
                raise ErrorDNIRepetido(persona.datos.nombre)

    def validar_cedula_unica(self, persona: object):
        if persona in self.incucai.cirujanos_especializados + self.incucai.cirujanos_generales:
            raise ErrorCedulaRepetido(persona.nombre)

    def validar_datos(self, objeto: object, campos_esperados: dict, opcionales: list = []):
        for campo, tipo_esperado in campos_esperados.items():
            valor = getattr(objeto, campo, None)

            if campo in opcionales:
                
                if valor is None:
                    continue

            if not isinstance(valor, tipo_esperado):
                raise ErrorTipoDatoInvalido(objeto.nombre,
                    campo,
                    f"{tipo_esperado.__name__} (recibido: {type(valor).__name__})"
            )
