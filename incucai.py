from transporte import Transporte
from gestor_cirujanos import GestorCirujanos
from gestor_donaciones import GestorDonaciones

class INCUCAI:
    """Sistema central"""

    def __init__(self):
        self.donantes = []
        self.receptores = []
        self.centros_salud = []
        self.cirujanos_esp = []
        self.cirujanos_gen = []
        self.vehiculos_terr = []
        self.aviones = []
        self.helic = []
        self.organos = []
        
        self.transporte = Transporte(self)
        self.gestor_cirujanos = GestorCirujanos(self)
        self.gestor_donaciones = GestorDonaciones(self)

    def registrar_donante(self, donante):
        # Validar centro de salud
        if donante.centro not in self.centros_salud:
            print(f"\n❌ Centro de salud del donante {donante.nombre} no está registrado.")
            return
        
        # Validar DNI único
        if donante in self.donantes + self.receptores:
            print(f"\n❌ El DNI de {donante.nombre} ya está registrado en el sistema.")
            return
        
        self.donantes.append(donante)
        print(f"\n✅ Donante {donante.nombre} registrado.")

    def registrar_organo(self, organo):
        self.organos.append(organo)

    def registrar_receptor(self, receptor):
        # Validar centro de salud
        if receptor.centro not in self.centros_salud:
            print(f"\n❌ Centro de salud del receptor {receptor.nombre} no está registrado.")
            return

        # Validar DNI único
        if receptor in self.donantes + self.receptores:
            print(f"\n❌ El DNI de {receptor.nombre} ya está registrado en el sistema.")
            return
        
        self.receptores.append(receptor)
        self.receptores = sorted(self.receptores)

        self.receptores=sorted(self.receptores)
        # Insertamos ordenando por prioridad y fecha
        print(f"\n✅ Receptor {receptor.nombre} registrado en lista de espera.")

    

    def registrar_centro(self, centro):
        self.centros_salud.append(centro)

    def registrar_cirujano_esp(self, cirujano):
        self.cirujanos_esp.append(cirujano)
        print(f"\n✅ Cirujano especializado {cirujano.nombre} registrado.")
        self.gestor_cirujanos.actualizar_datos()

    def registrar_cirujano_gen(self, cirujano):
        self.cirujanos_gen.append(cirujano)
        print(f"\n✅ Cirujano general {cirujano.nombre} registrado.")
        self.gestor_cirujanos.actualizar_datos()

    def registrar_vehiculo_terr(self, vehiculo_terr):
        self.vehiculos_terr.append(vehiculo_terr)

    def registrar_avion(self, avion):
        self.aviones.append(avion)

    def registrar_helic(self, helic):
        self.helic.append(helic)
    
    ##METODO MAGICO 2
    def __str__(self):
        return (
            f"\n------------------ ESTADO ACTUAL DEL SISTEMA -------------------\n"
            f"Donantes registrados: {len(self.donantes)}\n"
            f"Receptores en lista de espera: {len(self.receptores)}\n"
            f"Centros de salud registrados: {len(self.centros_salud)}\n"
            f"Cirujanos especializados disponibles: {len(self.cirujanos_esp)}\n"
            f"Cirujanos generales disponibles: {len(self.cirujanos_gen)}\n"
            f"Vehículos terrestres: {len(self.vehiculos_terr)}\n"
            f"Aviones disponibles: {len(self.aviones)}\n"
            f"Helicópteros disponibles: {len(self.helic)}\n"
            f"------------------------------------------------------------------\n"
        )


    def mostrar_lista_espera(self):
        print("\n--------------------------Lista de espera:---------------------------")
        for r in self.receptores:
            print(f"{r.nombre} - Órgano: {r.organo_r} - Fecha: {r.fecha_lista}")
        print("-----------------------------------------------------------------------\n")

    def realizar_transplante(self, donante, receptor, indice_organo):
        print(f"\n🩺 Trasplante realizado con éxito entre Donante {donante.nombre} y Receptor {receptor.nombre}")
        # Remover receptor de la lista de espera
        self.receptores.remove(receptor)
        # Actualizar órganos disponibles del donante
        donante.organos_d.pop(indice_organo)
        if not donante.organos_d:
            self.donantes.remove(donante)
            print(f"🗑️ Donante {donante.nombre} removido del sistema (sin órganos disponibles)")
    
    def match(self):
        """emparejar donantes y receptores"""
        self.gestor_cirujanos.normalizar_especialidades()
        self.gestor_cirujanos.actualizar_datos()
        self.gestor_donaciones.actualizar_indices()
        
        matches_realizados = False
        receptores_procesados = set() 
        
        receptores_pendientes = list(self.receptores)
        
        while receptores_pendientes:
            receptor = receptores_pendientes.pop(0)
            receptor_id = id(receptor)
            print(f"\n------------------------🔍 Evaluando receptor: {receptor.nombre}------------------------")

            # Verificar disponibilidad de cirujanos
            if not self.gestor_cirujanos.hay_cirujanos_en_centro(receptor.centro):
                print(f"\n❌ No hay cirujanos disponibles en el centro de {receptor.nombre}. Operación cancelada.")
                continue

            # Buscar donante compatible
            donante, indice_organo = self.gestor_donaciones.encontrar_donante_compatible(receptor)
            if not donante:
                print(f"\n❌ No se encontró donante compatible para {receptor.nombre}.")
                continue

            # Registrar ablación para donante vivo
            self.gestor_donaciones.registrar_ablacion_donante_vivo(donante, receptor.organo_r)
            print(f"\n✅ Match encontrado: Receptor {receptor.nombre} y Donante {donante.nombre}")

            # Transportar órgano si es necesario
            if donante.centro != receptor.centro:
                if not self.transporte.asignar_vehiculo(donante, receptor):
                    print("\n❌ No se pudo transportar el órgano. Match cancelado.")
                    continue
            else:
                print("\n✅ Donante y receptor en el mismo centro. No se requiere transporte.")

            # Evaluar operación
            if self.gestor_cirujanos.evaluar_operacion(receptor.centro, donante.organos_d[indice_organo]):
                print("\n✅ Operación exitosa")
                self.realizar_transplante(donante, receptor, indice_organo)
                matches_realizados = True
                receptores_procesados.add(receptor_id)  # Solo aquí se marca como procesado
            else:
                # Eliminar el órgano si la operación falló
                if 0 <= indice_organo < len(donante.organos_d):
                    organo_fallido = donante.organos_d.pop(indice_organo)
                    print(f"\n❌ Órgano {organo_fallido.nombre} descartado después de operación fallida")

                    # Eliminar donante si no tiene más órganos
                    if not donante.organos_d:
                        self.donantes.remove(donante)
                        print(f"🗑️ Donante {donante.nombre} removido del sistema (sin órganos disponibles)")

                # Reinsertar receptor con prioridad alta
                if receptor in self.receptores:
                    self.receptores.remove(receptor)
                self._insertar_receptor_ordenado(receptor)
                receptores_pendientes.insert(0, receptor)
