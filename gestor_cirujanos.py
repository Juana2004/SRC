from datetime import datetime
import random

class GestorCirujanos:
    """Gestiona la disponibilidad y asignación de cirujanos"""
    
    def __init__(self, incucai):
        self.incucai = incucai
        self._especialistas_por_centro = {}
        self._generales_por_centro = {}
        
    def actualizar_datos(self):
        self._especialistas_por_centro = {}
        self._generales_por_centro = {}
        
        for cirujano in self.incucai.cirujanos_esp:
            centro = cirujano.centro
            if centro not in self._especialistas_por_centro:
                self._especialistas_por_centro[centro] = []
            self._especialistas_por_centro[centro].append(cirujano)
            
        for cirujano in self.incucai.cirujanos_gen:
            centro = cirujano.centro
            if centro not in self._generales_por_centro:
                self._generales_por_centro[centro] = []
            self._generales_por_centro[centro].append(cirujano)
    
    def normalizar_especialidades(self):
        especialidad_map = {
            "cardiovascular": ["corazon"],
            "pulmonar": ["pulmon"],
            "traumatologo": ["huesos"],
            "plastico": ["piel", "corneas"],
            "gastroenterologo": ["instestino", "rinion", "higado", "pancreas"]
        }
        
        for cirujano in self.incucai.cirujanos_esp:
            if isinstance(cirujano.especialidad, str) and cirujano.especialidad in especialidad_map:
                cirujano.especialidad = especialidad_map[cirujano.especialidad]
    
    def hay_cirujanos_en_centro(self, centro) -> bool:
        """Verifica si hay cirujanos disponibles en un centro"""
        return (centro in self._especialistas_por_centro and self._especialistas_por_centro[centro]) or \
               (centro in self._generales_por_centro and self._generales_por_centro[centro])
    
    def evaluar_operacion(self, centro, organo) -> bool:
        """Evalúa si se puede realizar la operación con los cirujanos disponibles"""
        # Verificar viabilidad del órgano
        ahora = datetime.now()
        horas_desde_ablacion = int((ahora - organo.ablacion).total_seconds() // 3600)
        cir_dis = False
        
        if horas_desde_ablacion > 20:
            print("\n❌ No se puede realizar la operación: el órgano tiene más de 20 horas desde la ablación.")
            return False
            
        # Buscar cirujanos especialistas disponibles primero
        especialistas = self._especialistas_por_centro.get(centro, [])
        for cirujano in especialistas:
            if cirujano.operaciones_realizadas_hoy == 0:
                # Priorizar especialistas en el órgano específico
                es_especialista = isinstance(cirujano.especialidad, list) and organo.nombre in cirujano.especialidad
                umbral_exito = 3 if es_especialista else 5
                cir_dis = True
                print(f"\nLa operación la realiza el cirujano {cirujano.nombre}")
                
                if self._realizar_operacion(cirujano, umbral_exito):
                    return True
        
        # cirujanos generales
        generales = self._generales_por_centro.get(centro, [])
        for cirujano in generales:
            if cirujano.operaciones_realizadas_hoy == 0:
                print(f"\nLa operación la realiza el cirujano {cirujano.nombre}")
                cir_dis = True
                if self._realizar_operacion(cirujano, 5):  # Umbral más alto para generales
                    return True
        if not cir_dis:
            print("\n❌ No hay cirujanos disponibles para realizar la operación.")
        return False
    
    def _realizar_operacion(self, cirujano, umbral_exito) -> bool:
        """realización de la operación con probabilidad de éxito"""
        resultado = random.randint(1, 10)
        exito = resultado >= umbral_exito
        
        if exito:
            cirujano.operaciones_realizadas_hoy = 1
            return True
        else:
            print("\n❌ La operación falló")
            return False