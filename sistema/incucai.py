from sistema.transporte import Transporte
from sistema.gestor_cirujanos import GestorCirujanos
from sistema.gestor_donaciones import GestorDonaciones
from excepciones import ErrorDNIRepetido, ErrorCentroNoRegistrado


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
            raise ErrorCentroNoRegistrado(donante.nombre, donante.centro)
        
        # Validar DNI único
        if donante in self.donantes + self.receptores:
            raise ErrorDNIRepetido(donante.nombre)
        
        #el centro guarda a todos sus donadores
        self.donantes.append(donante)
        for centro in self.centros_salud:
            if centro.nombre == donante.centro.nombre:  
                centro.donantes.append(donante)
                break

        print(f"\n✔{donante.nombre}")

    def registrar_organo(self, organo):
        self.organos.append(organo)

    def registrar_receptor(self, receptor):
        # Validar centro de salud
        if receptor.centro not in self.centros_salud:
            raise ErrorCentroNoRegistrado(receptor.nombre, receptor.centro)

        # Validar DNI único
        if receptor in self.donantes + self.receptores:
            raise ErrorDNIRepetido(receptor.nombre)
        
        self.receptores.append(receptor)
        self.receptores.sort()  # Usa __lt__

        for centro in self.centros_salud:
            if centro.nombre == receptor.centro.nombre:  
                centro.receptores.append(receptor)
                break
        print(f"✔ {receptor.nombre}")


    

    def registrar_centro(self, centro):
        self.centros_salud.append(centro)

    def registrar_cirujano_esp(self, cirujano):
        self.cirujanos_esp.append(cirujano)
        print(f"✔{cirujano.nombre}")
        self.gestor_cirujanos.actualizar_datos()
        for centro in self.centros_salud:
            if centro.nombre == cirujano.centro.nombre:  
                centro.cirujanos.append(cirujano)
                break

    def registrar_cirujano_gen(self, cirujano):
        self.cirujanos_gen.append(cirujano)
        print(f"\n✔{cirujano.nombre}")
        self.gestor_cirujanos.actualizar_datos()
        for centro in self.centros_salud:
            if centro.nombre == cirujano.centro.nombre:  
                centro.cirujanos.append(cirujano)
                break

    def registrar_vehiculo_terr(self, vehiculo_terr):
        self.vehiculos_terr.append(vehiculo_terr)
        for centro in self.centros_salud:
            if centro.nombre == vehiculo_terr.centro.nombre:  
                centro.vehiculos.append(vehiculo_terr)
                break

    def registrar_avion(self, avion):
        self.aviones.append(avion)
        for centro in self.centros_salud:
            if centro.nombre == avion.centro.nombre:  
                centro.vehiculos.append(avion)
                break

    def registrar_helic(self, helic):
        self.helic.append(helic)
        for centro in self.centros_salud:
            if centro.nombre == helic.centro.nombre:  
                centro.vehiculos.append(helic)
                break
    
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

    def receptores_encentro(self, centro):
        for c in self.centros_salud:
            if c == centro:  #__eq__
                nombres = [receptor.nombre for receptor in c.receptores]
                print(nombres)
                

        ##buscar un receptor e informar q prioridad tiene
    def prioridad_receptor(self, receptor):
        if receptor in self.receptores:
            posicion = self.receptores.index(receptor)
            print(f"El receptor {receptor.nombre} está en el lugar {posicion + 1} de la lista de espera.")
        else:
            print("El receptor no está en la lista de espera.")


        ##mostrar lista de donantes
    def mostrar_lista_donantes(self):
        print("\n--------------------------Lista de espera:---------------------------")
        for r in self.donantes:
            print(f"{r.nombre} ")
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

            # Verificar disponibilidad de cirujanos en centro receptor
            if not self.gestor_cirujanos.hay_cirujanos_en_centro(receptor.centro):
                print(f"\n❌ No hay cirujanos disponibles en el centro de {receptor.nombre}. Operación cancelada.")
                continue

            # Buscar donante compatible
            donante, indice_organo = self.gestor_donaciones.encontrar_donante_compatible(receptor)
            if not donante:
                print(f"\n❌ No se encontró donante compatible para {receptor.nombre}.")
                continue

            print(f"\n✅ Match encontrado: Receptor {receptor.nombre} y Donante {donante.nombre}")

            # Transportar órgano si es necesario
            if donante.centro != receptor.centro:
                if not self.transporte.asignar_vehiculo(donante, receptor):
                    print("\n❌ No se pudo transportar el órgano. Match cancelado.")
                    continue
            else:
                print("\n✅ Donante y receptor en el mismo centro. No se requiere transporte.")

            # Evaluar operación
            if self.gestor_cirujanos.evaluar_operacion(receptor.centro, donante.organos_d[indice_organo], receptor):
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
                receptores_pendientes.insert(0, receptor)
