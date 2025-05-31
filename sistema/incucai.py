from localizables.centro_de_salud import CentroDeSalud
from datetime import date
from excepciones import *
from .validaciones import Validaciones
from typing import Optional



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
        self.validaciones = Validaciones(self)

    def _encontrar_centro_por_nombre(
        self, nombre_centro: str
    ) -> Optional[CentroDeSalud]:
        """
        Encuentra el objeto centro a partir de su nombre
        Args:
        nombre_centro: string
        Return:
        objeto del tipo CentroDeSalud
        """
        if nombre_centro in self._centros_por_nombre:
            return self._centros_por_nombre[nombre_centro]
        for centro in self.centros_salud:
            if centro.nombre == nombre_centro:
                self._centros_por_nombre[nombre_centro] = centro
                return centro
        return None

    def _agregar_persona_a_centro(self, persona: object, lista_centro_attr: str):
        """
        Agrega una persona a la lista del centro
        Args:
        persona: objeto
        lista_centro_attr: str
        """
        centro = self._encontrar_centro_por_nombre(persona.centro.nombre)
        if centro:
            getattr(centro, lista_centro_attr).append(persona)
        else:
            raise ValueError(
                f"Centro '{persona.centro.nombre}' no encontrado para la persona '{persona.nombre}'"
            )

    """
    A partir de aca todos los metodos registran a su respectivo argumento en las listas de incucai y si corresponde del centro
    Args:
        object
    """

    def registrar_donante(self, donante: object):
        self.validaciones.validar_centro_registrado(donante)
        self.validaciones.validar_dni_unico(donante)
        self.validaciones.validar_datos(
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
            },
            opcionales=["fecha_fallecimiento"],
        )
        self.donantes.append(donante)
        self._agregar_persona_a_centro(donante, "donantes")
        print(f"✔{donante.nombre}")

    def registrar_organo(self, organo: object):
        self.organos.append(organo)

    def registrar_receptor(self, receptor: object):
        self.validaciones.validar_centro_registrado(receptor)
        self.validaciones.validar_dni_unico(receptor)
        self.validaciones.validar_datos(
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
            },
        )
        self.receptores.append(receptor)
        self.receptores.sort()
        self._agregar_persona_a_centro(receptor, "receptores")
        print(f"✔{receptor.nombre}")

    def registrar_centro(self, centro: object):
        self.centros_salud.append(centro)
        self._centros_por_nombre[centro.nombre] = centro

    def _registrar_cirujano(
        self, cirujano: object, lista_cirujanos: list[object], tipo_cirujano: str
    ):
        self.validaciones.validar_centro_registrado(cirujano)
        self.validaciones.validar_dni_unico(cirujano)
        self.validaciones.validar_datos(
            cirujano,
            {
                "nombre": str,
                "cedula": int,
                "centro": CentroDeSalud,
                "especialidad": str,
            },
            opcionales=["especialidad"],
        )
        lista_cirujanos.append(cirujano)
        self._agregar_persona_a_centro(cirujano, "cirujanos")
        print(f"✔{tipo_cirujano}: {cirujano.nombre}")

    def registrar_cirujano_especializado(self, cirujano: object):
        self._registrar_cirujano(
            cirujano, self.cirujanos_especializados, "especializado"
        )

    def registrar_cirujano_general(self, cirujano: object):
        self._registrar_cirujano(cirujano, self.cirujanos_generales, "general")

    def _registrar_vehiculo(self, vehiculo: object, lista_vehiculos: list[object]):
        lista_vehiculos.append(vehiculo)
        centro = self._encontrar_centro_por_nombre(vehiculo.centro.nombre)
        if centro:
            centro.vehiculos.append(vehiculo)

    def registrar_vehiculo_terrestre(self, vehiculo_terrestre: object):
        self._registrar_vehiculo(vehiculo_terrestre, self.vehiculos_terrestres)

    def registrar_avion(self, avion: object):
        self._registrar_vehiculo(avion, self.aviones)

    def registrar_helicoptero(self, helicoptero: object):
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
        )
        salida += f"{'-' * 60}\nLISTA DE DONANTES\n"
        if not self.donantes:
            salida += "No hay donantes registrados.\n"
        else:
            for i, donante in enumerate(self.donantes, 1):
                organos_disponibles = (
                    len(donante.organos_donante)
                    if hasattr(donante, "organos_donante")
                    else 0
                )
                salida += f"{i:2d}. {donante.nombre} ({organos_disponibles} órganos disponibles)\n"
        salida += f"{'-' * 60}\nLISTA DE RECEPTORES\n"
        if not self.receptores:
            salida += "No hay receptores en lista de espera.\n"
        else:
            for i, receptor in enumerate(self.receptores, 1):
                salida += (
                    f"{i:2d}. {receptor.nombre:<20} | Órgano: {receptor.organo_receptor:<15} "
                    f"| Fecha: {receptor.fecha_lista}\n"
                )
        return salida

    def _obtener_receptores_por_centro(self, centro: CentroDeSalud) -> list:
        """
        Obtiene la lista de receptores de un centro
        Args:
        centro: object
        Return:
        lista
        """
        centro_encontrado = self._encontrar_centro_por_nombre(centro.nombre)
        if centro_encontrado:
            return [receptor.nombre for receptor in centro_encontrado.receptores]
        return []

    def mostrar_receptores_por_centro(self, centro: CentroDeSalud):
        """
        Muestra los receptores de un centro
        Args:
        centro: object
        """
        receptores = self._obtener_receptores_por_centro(centro)
        print(f"\n--- Receptores en {centro.nombre} ---")
        if receptores:
            for i, nombre in enumerate(receptores, 1):
                print(f"{i}. {nombre}")
        else:
            print("No hay receptores en este centro.")

    def _obtener_prioridad_receptor(self, receptor: object) -> Optional[int]:
        """
        Obtiene la posicion de un receptor en lista de espera
        Args:
        receptor: object
        Return:
        int o NOne
        """
        try:
            posicion = self.receptores.index(receptor)
            return posicion + 1
        except ValueError:
            return None

    def mostrar_prioridad_receptor(self, receptor: object):
        """
        Muestra la prioridad del receptor
        """
        prioridad = self._obtener_prioridad_receptor(receptor)
        if prioridad:
            print(
                f"📍 El receptor {receptor.nombre} está en el lugar {prioridad} de la lista de espera."
            )
        else:
            print(f"❌ El receptor {receptor.nombre} no está en la lista de espera.")
