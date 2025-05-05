

class Cirujano():
    def __init__(self, nombre, matricula, especialidad, centro):
        self.nombre = nombre
        self.matricula = matricula
        self.centro = centro   
        self.especialidad = especialidad           
        self.operacion_hoy = False        # controla si ya hizo una operación hoy

    def esta_disponible(self):
        #Devuelve True si no opero hoy
        return not self.operacion_hoy

    def asignar_operacion(self):
        #Marca que ya opero hoy y no podrá operar de nuevo
        if self.operacion_hoy:
            raise Exception(f"{self.nombre} ya realizó una operación hoy.")
        self.operacion_hoy = True

    def resetear_disponibilidad(self):
        #Al inicio de cada día, resetear para permitir nuevas operaciones
        self.operacion_hoy = False

    def __str__(self):
        return f"Dr/a {self.nombre} (DNI {self.dni})  – Centro: {self.centro.nombre}"
