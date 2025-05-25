from localizables.centro_de_salud import CentroDeSalud
from datetime import date
from excepciones import ErrorCedulaRepetido, ErrorCentroNoRegistrado, ErrorDNIRepetido, ErrorTipoDatoInvalido


class INCUCAI:
    def __init__(self):
        self.donantes: list[object] = []
        self.receptores: list[object] = []
        self.organos: list[object] = []
        self.centros_salud: list[object] = []
        self._centros_por_nombre: dict = {}
        self.cirujanos_especializados: list[object] = []
        self.cirujanos_generales: list[object] = []
        self.vehiculos_terrestres: list[object] = []
        self.aviones: list[object] = []
        self.helicopteros: list[object] = []

    def _encontrar_centro_por_nombre(self, nombre_centro: str):
        if nombre_centro in self._centros_por_nombre:
            return self._centros_por_nombre[nombre_centro]
        for centro in self.centros_salud:
            if centro.nombre == nombre_centro:
                self._centros_por_nombre[nombre_centro] = centro
                return centro
        return None

    def _agregar_persona_a_centro(self, persona: object, lista_centro_attr: str):
        centro = self._encontrar_centro_por_nombre(persona.centro.nombre)
        if centro:
            getattr(centro, lista_centro_attr).append(persona)
        else:
            raise ValueError(f"Centro '{persona.centro.nombre}' no encontrado para la persona '{persona.nombre}'")
        
    def validar_centro_registrado(self, persona: object):
        if persona.centro not in self.centros_salud:
            raise ErrorCentroNoRegistrado(persona.nombre, persona.centro)

    def validar_dni_unico(self, persona: object):
        if persona in self.donantes + self.receptores:
            raise ErrorDNIRepetido(persona.nombre)
    
    def validar_cedula_unica(self, persona: object):
        if persona in self.cirujanos_especializados + self.cirujanos_generales:
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



    def registrar_donante(self, donante: object):
        
        self.validar_centro_registrado( donante)
        self.validar_dni_unico(donante)
        self.validar_datos(
        donante,
        {
            "nombre": str,
            "dni": int,
            "centro": CentroDeSalud,
            "fecha_nacimiento": date,
            "sexo": str,
            "telefono": int,
            "tipo_sangre": str,
            "fecha_fallecimiento": date,
            "organos_donante": list,
        }, opcionales= ["fecha_fallecimiento"]
        )
        self.donantes.append(donante)
        self._agregar_persona_a_centro(donante, "donantes")
        print(f"✔{donante.nombre}")

    def registrar_organo(self, organo: object):
        self.organos.append(organo)

    def registrar_receptor(self, receptor: object):
        self.validar_centro_registrado(receptor)
        self.validar_dni_unico(receptor)
        self.validar_datos(
        receptor,
        {
            "nombre": str,
            "dni": int,
            "fecha_nacimiento": date,
            "sexo": str,
            "telefono": int,
            "tipo_sangre": str,
            "centro": CentroDeSalud,
            "organo_receptor": str,
            "fecha_lista": date,
            "patologia": str,
            "urgencia": bool,
        }
        )
        self.receptores.append(receptor)
        self.receptores.sort()
        self._agregar_persona_a_centro(receptor, "receptores")
        print(f"✔{receptor.nombre}")

    def registrar_centro(self, centro: object):
        self.centros_salud.append(centro)
        self._centros_por_nombre[centro.nombre] = centro

    def _registrar_cirujano(self, cirujano, lista_cirujanos, tipo_cirujano):
        self.validar_centro_registrado(cirujano)
        self.validar_dni_unico(cirujano)
        self.validar_datos(
        cirujano,
        {
            "nombre": str,
            "cedula": int,
            "centro": CentroDeSalud,
            "especialidad": str,
        }, opcionales= ["especialidad"]
        )
        lista_cirujanos.append(cirujano)
        self._agregar_persona_a_centro(cirujano, "cirujanos")
        print(f"✔{tipo_cirujano}: {cirujano.nombre}")

    def registrar_cirujano_especializado(self, cirujano):
        self._registrar_cirujano(
            cirujano, self.cirujanos_especializados, "especializado"
        )

    def registrar_cirujano_general(self, cirujano):
        self._registrar_cirujano(cirujano, self.cirujanos_generales, "general")

    def _registrar_vehiculo(self, vehiculo, lista_vehiculos):
        lista_vehiculos.append(vehiculo)
        centro = self._encontrar_centro_por_nombre(vehiculo.centro.nombre)
        if centro:
            centro.vehiculos.append(vehiculo)

    def registrar_vehiculo_terrestre(self, vehiculo_terrestre):
        self._registrar_vehiculo(vehiculo_terrestre, self.vehiculos_terrestres)

    def registrar_avion(self, avion):
        self._registrar_vehiculo(avion, self.aviones)

    def registrar_helicoptero(self, helicoptero):
        self._registrar_vehiculo(helicoptero, self.helicopteros)

    def __str__(self):
        salida = (
            f"\n{'-' * 60}\n"
            f"ESTADO ACTUAL DEL SISTEMA INCUCAI\n"
            f" Donantes registrados: {len(self.donantes)}\n"
            f" Receptores en lista de espera: {len(self.receptores)}\n"
            f" Centros de salud registrados: {len(self.centros_salud)}\n"
            f" Cirujanos especializados: {len(self.cirujanos_especializados)}\n"
            f" Cirujanos generales: {len(self.cirujanos_generales)}\n"
            f" Vehículos terrestres: {len(self.vehiculos_terrestres)}\n"
            f" Aviones disponibles: {len(self.aviones)}\n"
            f" Helicópteros disponibles: {len(self.helicopteros)}\n"
            f"\n{'-' * 60}\n"
            f"LISTA DE ESPERA\n"
        )
        if not self.receptores:
            salida += "No hay receptores en lista de espera.\n"
        else:
            for i, receptor in enumerate(self.receptores, 1):
                salida += (
                    f"{i:2d}. {receptor.nombre:<20} | Órgano: {receptor.organo_receptor:<15} "
                    f"| Fecha: {receptor.fecha_lista}\n"
                )
        salida += f"{'-' * 60}\nLISTA DE DONANTES\n"
        if not self.donantes:
            salida += "No hay donantes registrados.\n"
        else:
            for i, donante in enumerate(self.donantes, 1):
                organos_disponibles = (
                    len(donante.organos_d) if hasattr(donante, "organos_d") else 0
                )
                salida += f"{i:2d}. {donante.nombre} ({organos_disponibles} órganos disponibles)\n"
        salida += f"{'-' * 60}\n"
        return salida

    def obtener_receptores_por_centro(self, centro):
        centro_encontrado = self._encontrar_centro_por_nombre(centro.nombre)
        if centro_encontrado:
            return [receptor.nombre for receptor in centro_encontrado.receptores]
        return []

    def mostrar_receptores_por_centro(self, centro):
        receptores = self.obtener_receptores_por_centro(centro)
        print(f"\n--- Receptores en {centro.nombre} ---")
        if receptores:
            for i, nombre in enumerate(receptores, 1):
                print(f"{i}. {nombre}")
        else:
            print("No hay receptores en este centro.")

    def obtener_prioridad_receptor(self, receptor):
        try:
            posicion = self.receptores.index(receptor)
            return posicion + 1
        except ValueError:
            return None

    def mostrar_prioridad_receptor(self, receptor):
        prioridad = self.obtener_prioridad_receptor(receptor)
        if prioridad:
            print(
                f"📍 El receptor {receptor.nombre} está en el lugar {prioridad} de la lista de espera."
            )
        else:
            print(f"❌ El receptor {receptor.nombre} no está en la lista de espera.")

