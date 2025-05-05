class Persona:


    def __init__(self, nombre, dni, fecha_nacimiento, tipo_sangre):
        self.nombre = nombre
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento  # dd/mm/aaaa
        self.tipo_sangre = tipo_sangre 

    def __str__(self):
        return f"{self.nombre} (DNI: {self.dni}) - Sangre: {self.tipo_sangre}"

    def edad(self):
        from datetime import datetime
        dia, mes, año = map(int, self.fecha_nacimiento.split("/"))
        hoy = datetime.now()
        edad = hoy.year - año - ((hoy.month, hoy.day) < (mes, dia))
        return edad
