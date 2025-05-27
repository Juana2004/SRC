from datetime import datetime, timedelta
import random
from localizables.centro_de_salud import CentroDeSalud
from pacientes.receptor import Receptor
from typing import Optional
from pacientes.donante_vivo import DonanteVivo
from pacientes.paciente import Paciente
from pacientes.receptor import Receptor
from cirujanos.cirujano import Cirujano


class GestorCirujanos:

    def __init__(self, incucai):
        self.incucai = incucai

    def normalizar_especialidades(self):
        '''
        Modifica el atributo especialidad de los cirujanos especializados por una lista de órganos correspondiente a esta.
        ''' 
    
        especialidad_map = {
            "cardiovascular": ["corazon"],
            "pulmonar": ["pulmon"],
            "traumatologo": ["huesos"],
            "plastico": ["piel", "corneas"],
            "gastroenterologo": ["instestino", "rinion", "higado", "pancreas"],
        }

        for cirujano in self.incucai.cirujanos_especializados:
            if (
                isinstance(cirujano.especialidad, str)
                and cirujano.especialidad in especialidad_map
            ):
                cirujano.especialidad = especialidad_map[cirujano.especialidad]

    def hay_cirujanos_en_centro(self, centro: CentroDeSalud) -> bool:
        '''
        Verifica si la lista de cirujanos del centro contiene al menos uno
        Args:
            centro: CentroDeSalud
        Returns:
            bool
        '''
        if centro.cirujanos != []:
            return True
        else:
            return False


    def evaluar_operacion(
        self,
        centro: CentroDeSalud,
        organo: object,
        receptor: Receptor,
        tiempo_transporte: float,
    ) -> bool:
        """
        Evalúa si es posible realizar una operación de trasplante en un centro de salud,
        considerando la disponibilidad de cirujanos, el tiempo desde la ablación del órgano,
        y la probabilidad de éxito según la especialidad del cirujano.
        Args:
            centro: CentroDeSalud
            organo: object
            receptor: Receptor
            tiempo_transporte: float
        Returns:
            bool: True si la operación se realizó con éxito, False en caso contrario
        """

        self.cirujano_disponible = False

        if self._horas_desde_ablacion(tiempo_transporte, organo) > 20:
            print(
                "\n❌ No se puede realizar la operación: el órgano tiene más de 20 horas desde la ablación."
            )
            return False

        especialistas = [
            c for c in centro.cirujanos if getattr(c, "especialidad", None) is not None
        ]
        generales = [c for c in centro.cirujanos if not hasattr(c, "especialidad")]

        for cirujano in especialistas:
            if cirujano.operaciones_realizadas_hoy == 0:
                es_especialista = (
                    isinstance(cirujano.especialidad, list)
                    and organo.nombre in cirujano.especialidad
                )
                umbral_exito = 3 if es_especialista else 5
                if self._realizar_operacion(cirujano, umbral_exito, receptor):
                    return True

        for cirujano in generales:
            if cirujano.operaciones_realizadas_hoy == 0:
                umbral_exito = 5
                if self._realizar_operacion(cirujano, umbral_exito, receptor):
                    return True

        if not self.cirujano_disponible:
            print("\n❌ No hay cirujanos disponibles para realizar la operación.")

        return False

    def _realizar_operacion(self, cirujano: Cirujano, umbral_exito: int, receptor: Receptor) -> bool:
        '''
        Metodo privado
        Imprime el cirujano encargado de la operacion, le registra a este que realizo una operacion.
        Modifico el estado de la variable cirujano_disponible, indicando que hay al menos un cirujano disponible.
        Verifica si el metodo _umbral_operacion se cumple.
        Args:
            cirujano: Objeto heredado de Cirujano
            umbral_exito: int 
            receptor: Receptor
        Returns:
            bool
        '''
        print(f"\nLa operación la realiza el cirujano {cirujano.nombre}")
        cirujano.operaciones_realizadas_hoy = 1
        self.cirujano_disponible = True
        if self._umbral_operacion(umbral_exito, receptor):
            return True
        else: 
            return False

    def _umbral_operacion(self, umbral_exito: int, receptor: Receptor) -> bool:
        '''
        Metodo privado
        Recibe un entero que representa el umbral de exito y un objeto de tipo receptor.
        Genera un numero, utilizando la libreria random, entre 1 y 10.
        Define la variable de tipo booleano "exito", que sera verdadera cuando el resultado sea >= al umbral de exito.
        Si "exito" es verdadera retorna el bool True.
        Si "exito" es falsa imprime que la operacion fallo, cambia el estado del receptor a inestable y retorna el bool False.
        '''
        resultado = random.randint(1, 10)
        exito = resultado >= umbral_exito
        if exito:
            return True
        else:
            print("\n❌ La operación falló")
            receptor.estado = "inestable"
            return False

    def _horas_desde_ablacion(self, tiempo_transporte, organo):
        ahora = datetime.now()
        fecha_hora_ablacion = datetime.combine(
            organo.fecha_ablacion, organo.hora_ablacion
        )
        delta_transporte = timedelta(hours=tiempo_transporte)
        horas_desde_ablacion = int(
            (ahora - delta_transporte - fecha_hora_ablacion).total_seconds() // 3600
        )
        return horas_desde_ablacion

    ##a partir de aca pertence a operacion donante

    def cirujanos_disponibles_ablacion(self, donante: object) -> Optional[list[object]]:
        centro = donante.centro
        cirujanos_disponibles = [
            c for c in centro.cirujanos if c.operaciones_realizadas_hoy == 0
        ]
        return cirujanos_disponibles

    def realizar_operacion_ablacion(self, cirujano: object, donante, receptor):
        print(f"El cirujano {cirujano.nombre} realiza la ablación")
        cirujano.operaciones_realizadas_hoy = 1
        organo_requerido = receptor.organo_receptor
        self._registrar_ablacion_donante_vivo(donante, organo_requerido)

    def _registrar_ablacion_donante_vivo(
        self, donante: object, organo_requerido: str
    ):  ##
        if isinstance(donante, DonanteVivo):
            fecha_actual = datetime.now()
            donante.fecha_ablacion = fecha_actual
            donante.hora_ablacion = fecha_actual.time()

            for organo in donante.organos_donante:
                if organo.nombre == organo_requerido:
                    organo.fecha_ablacion = fecha_actual
                    organo.hora_ablacion = fecha_actual.time()
                    break
