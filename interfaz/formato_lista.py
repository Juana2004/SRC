from abc import ABC
class FormatoListaDeEspera(ABC):
    """Formateador de contenido para la lista de espera"""

    def __init__(self):
        if type(self) is FormatoListaDeEspera:
            raise TypeError("FormatoListaDeEspera es una clase abstracta y no puede ser instanciada directamente.")
        super().__init__()

    @staticmethod
    def formato_lista(self, contenido):
        '''
        Metodo abstracto
        Formato visual del contenido de la lista de espera
        '''
        if not contenido.strip():
            return " No hay pacientes en lista de espera"
        
        lineas = contenido.split('\n')
        lineas_formateadas = []
        
        for linea in lineas:
            if not linea.strip():
                lineas_formateadas.append("")
                continue
            
            linea_formateada = self._formato_linea(linea)
            lineas_formateadas.append(linea_formateada)
        
        return "\n".join(lineas_formateadas)
    
    def _formato_linea(self, linea):
        '''
        Metodo Privado
        Formatea una línea individual según su contenido
        '''
        linea_lower = linea.lower()

        if linea.startswith('='):
            return "=" * 70
        elif linea.startswith('-'):
            return "-" * 70
        elif any(keyword in linea_lower for keyword in ['paciente', 'id', 'nombre', 'edad']):
            return f"📋 {linea}"
        elif any(keyword in linea_lower for keyword in ['urgente', 'crítico', 'prioridad']):
            return f"🚨 {linea}"
        elif any(keyword in linea_lower for keyword in ['compatible', 'match']):
            return f"✅ {linea}"
        else:
            return f"{linea}"
    
    @staticmethod
    def count_patients(self, contenido):
        '''
        Metodo abstracto
        Cuenta el número de pacientes en la lista en la lista
        '''
        if not contenido.strip():
            return 0
        
        lineas = [linea.strip() for linea in contenido.split('\n') if linea.strip()]
        paciente_lineas = [l for l in lineas 
                        if not l.startswith('-') 
                        and not l.startswith('=') 
                        and l]
        return len(paciente_lineas)