from datetime import datetime, timedelta
import random



class GestorCirujanos:
    """Gestiona la disponibilidad y asignación de cirujanos"""

    def __init__(self, incucai):
        self.incucai = incucai

    def normalizar_especialidades(self):
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

    def hay_cirujanos_en_centro(self, centro) -> bool:
        if centro.cirujanos != []:
            return True
        else:
            return False

    def evaluar_operacion(self, centro, organo, receptor, tiempo_transporte) -> bool:
        """Evalúa si se puede realizar la operación con los cirujanos disponibles"""
        
        ahora = datetime.now()
        fecha_hora_ablacion = datetime.combine(organo.fecha_ablacion, organo.hora_ablacion)
        delta_transporte = timedelta(hours=tiempo_transporte)
        horas_desde_ablacion = int((ahora - delta_transporte - fecha_hora_ablacion).total_seconds() // 3600)
        cir_dis = False

        if horas_desde_ablacion > 20:
            print("\n❌ No se puede realizar la operación: el órgano tiene más de 20 horas desde la ablación.")
            return False

        especialistas = [c for c in centro.cirujanos if getattr(c, 'especialidad', None) is not None]
        generales = [c for c in centro.cirujanos if not hasattr(c, 'especialidad')]
        for cirujano in especialistas:
            if cirujano.operaciones_realizadas_hoy == 0:
                es_especialista = (
                    isinstance(cirujano.especialidad, list)
                    and organo.nombre in cirujano.especialidad
                )
                umbral_exito = 3 if es_especialista else 5
                cir_dis = True
                print(f"\nLa operación la realiza el cirujano {cirujano.nombre}")
                cirujano.operaciones_realizadas_hoy = 1
                if self._realizar_operacion(cirujano, umbral_exito, receptor):
                    return True

        for cirujano in generales:
            if cirujano.operaciones_realizadas_hoy == 0:
                print(f"\nLa operación la realiza el cirujano {cirujano.nombre}")
                cirujano.operaciones_realizadas_hoy = 1
                cir_dis = True
                if self._realizar_operacion(
                    cirujano, 5, receptor
                ):  
                    return True
        if not cir_dis:
            print("\n❌ No hay cirujanos disponibles para realizar la operación.")
        return False

    def _realizar_operacion(self, cirujano, umbral_exito, receptor) -> bool:
        """realización de la operación con probabilidad de éxito"""
        resultado = random.randint(1, 10)
        exito = resultado >= umbral_exito
        if exito:
            return True
        else:
            print("\n❌ La operación falló")
            receptor.estado = "inestable"
            return False

    def cirujanos_disponibles_ablacion(self, donante):
        centro = donante.centro
        cirujanos_disponibles = [c for c in centro.cirujanos if c.operaciones_realizadas_hoy == 0]
        return cirujanos_disponibles

    def realizar_operacion_ablacion(self, cirujano):
        print(f"El cirujano {cirujano.nombre} realiza la ablación")
        cirujano.operaciones_realizadas_hoy = 1
