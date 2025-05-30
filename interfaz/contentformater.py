class ContentFormatter:
    """Formateador de contenido para la lista de espera"""
    @staticmethod
    def format_wait_list(content):
        """Mejora el formato visual del contenido de la lista de espera"""
        if not content.strip():
            return "📋 No hay pacientes en lista de espera"
        
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            if not line.strip():
                formatted_lines.append("")
                continue
            
            formatted_line = ContentFormatter._format_line(line)
            formatted_lines.append(formatted_line)
        
        return "\n".join(formatted_lines)
    
    @staticmethod
    def _format_line(line):
        """Formatea una línea individual según su contenido"""
        line_lower = line.lower()

        if line.startswith('='):
            return "=" * 70
        elif line.startswith('-'):
            return "-" * 70
        elif any(keyword in line_lower for keyword in ['paciente', 'id', 'nombre', 'edad']):
            return f"📋 {line}"
        elif any(keyword in line_lower for keyword in ['urgente', 'crítico', 'prioridad']):
            return f"🚨 {line}"
        elif any(keyword in line_lower for keyword in ['compatible', 'match']):
            return f"✅ {line}"
        else:
            return f"   {line}"
    
    @staticmethod
    def count_patients(content):
        """Cuenta el número de pacientes en la lista"""
        if not content.strip():
            return 0
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        patient_lines = [l for l in lines 
                        if not l.startswith('-') 
                        and not l.startswith('=') 
                        and l]
        return len(patient_lines)