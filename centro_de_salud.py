class CentroDeSalud:


    def __init__(self, nombre, direccion, partido, provincia):
        self.nombre = nombre
        self.direccion = direccion
        self.partido = partido
        self.provincia = provincia
        self.pacientes = [] 
        self.medicos = []    

    def agregar_paciente(self, paciente):
        self.pacientes.append(paciente)

    def listar_pacientes(self):
        print(f"\nPacientes en {self.nombre}:")
        for p in self.pacientes:
            print(f"- {p.nombre} ({type(p).__name__})")

    def __str__(self):
        return f"{self.nombre} - {self.direccion} - {len(self.pacientes)} pacientes"
