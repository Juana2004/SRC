from sistema.transporte import Transporte
from sistema.gestor_cirujanos import GestorCirujanos
from sistema.gestor_donaciones import GestorDonaciones
from excepciones import ErrorDNIRepetido, ErrorCentroNoRegistrado, ErrorCedulaRepetido, ErrorTipoDatoInvalido
from localizables.centro_de_salud import CentroDeSalud
from datetime import date
from organos.organo import Organo
from organos.organo_vivo import OrganoVivo



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

        self.transporte: object = Transporte(self)
        self.gestor_cirujanos: object = GestorCirujanos(self)
        self.gestor_donaciones: object = GestorDonaciones(self)

    def _validar_centro_registrado(self, persona: object):
        if persona.centro not in self.centros_salud:
            raise ErrorCentroNoRegistrado(persona.nombre, persona.centro)

    def _validar_dni_unico(self, persona: object):
        if persona in self.donantes + self.receptores:
            raise ErrorDNIRepetido(persona.nombre)
    
    def _validar_cedula_unica(self, persona: object):
        if persona in self.cirujanos_especializados + self.cirujanos_generales:
            raise ErrorCedulaRepetido(persona.nombre)

    def _validar_datos(self, objeto: object, campos_esperados: dict, opcionales: list = []):
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


    def registrar_donante(self, donante: object):
        self._validar_centro_registrado(donante)
        self._validar_dni_unico(donante)
        self._validar_datos(
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
        self._validar_centro_registrado(receptor)
        self._validar_dni_unico(receptor)
        self._validar_datos(
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
        self._validar_datos(
        centro,
        {
            "nombre": str, 
            "direccion": str, 
            "partido": str, 
            "provincia": str, 
            "pais": str 
        }
        )

    def _registrar_cirujano(self, cirujano, lista_cirujanos, tipo_cirujano):
        self._validar_centro_registrado(cirujano)
        self._validar_cedula_unica(cirujano)
        self._validar_datos(
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

    def realizar_transplante(self, donante, receptor, indice_organo):
        print(
            f"Trasplante entre {donante.nombre} y {receptor.nombre} realizado con éxito"
        )
        centro_receptor = receptor.centro
        centro_donante = donante.centro
        self.receptores.remove(receptor)
        centro_receptor.receptores.remove(receptor)
        if 0 <= indice_organo < len(donante.organos_donante):
            donante.organos_donante.pop(indice_organo)
            if not donante.organos_donante and donante in self.donantes:
                self.donantes.remove(donante)
                centro_donante.donantes.remove(donante)
                print(f"🗑️ Donante {donante.nombre} removido del sistema.")

    def match(self):
        self.gestor_cirujanos.normalizar_especialidades()

        matches_realizados = False
        receptores_procesados = set()
        receptores_pendientes = list(self.receptores)

        while receptores_pendientes:
            receptor = receptores_pendientes.pop(0)
            receptor_id = id(receptor)  

            print(f"\nEvaluando receptor: {receptor.nombre}")

            if not self.gestor_cirujanos.hay_cirujanos_en_centro(receptor.centro):
                print(f"\n❌ No hay cirujanos disponibles en el centro de {receptor.nombre}\n")
                continue

            donante, indice_organo = (self.gestor_donaciones.encontrar_donante_compatible(receptor))

            if not donante:
                print(f"\n❌ No se encontró donante compatible para {receptor.nombre}\n")
                continue

            print(f"✅ Match encontrado: {receptor.nombre} ↔ {donante.nombre}")

            exito_transporte, tiempo_transporte = self.gestionar_transporte(donante, receptor)
            if not exito_transporte:
                continue

            if self._ejecutar_operacion(donante, receptor, indice_organo, tiempo_transporte):
                matches_realizados = True
                receptores_procesados.add(receptor_id)
            else:
                self._manejar_operacion_fallida(
                    donante, receptor, indice_organo, receptores_pendientes
                )
        return matches_realizados

    def gestionar_transporte(self, donante, receptor) -> tuple[bool, float]:
        if donante.centro != receptor.centro:
            exito, tiempo = self.transporte.asignar_vehiculo(donante, receptor)
            if not exito:
                print("❌ No se pudo transportar el órgano. Match cancelado.")
                return False, 0.0
            else:
                return True, tiempo
        else:
            print("✅ Donante y receptor en el mismo centro. No se requiere transporte.")
            return True, 0.0 

    def _ejecutar_operacion(self, donante, receptor, indice_organo, tiempo_transporte):
        if self.gestor_cirujanos.evaluar_operacion(
            receptor.centro, donante.organos_donante[indice_organo], receptor, tiempo_transporte):
            print("✅ Operación exitosa")
            self.realizar_transplante(donante, receptor, indice_organo)
            return True
        return False

    def _manejar_operacion_fallida(self, donante, receptor, indice_organo, receptores_pendientes):
        centro_donante = donante.centro
        if 0 <= indice_organo < len(donante.organos_donante):
            organo_fallido = donante.organos_donante.pop(indice_organo)
            print(
                f"❌ Órgano {organo_fallido.nombre} descartado después de operación fallida"
            )
            if not donante.organos_donante and donante in self.donantes:
                self.donantes.remove(donante)
                centro_donante.donantes.remove(donante)
                print(f"🗑️ Donante {donante.nombre} removido del sistema (sin órganos disponibles)")
        if receptor in self.receptores:
            self.receptores.remove(receptor)
        receptores_pendientes.insert(0, receptor)
