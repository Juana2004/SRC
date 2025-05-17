from datetime import datetime
import random
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="incucai_app")
from geopy.distance import distance
from organo import Organo

class INCUCAI:

    def __init__(self):
        self.donantes = []
        self.receptores = []
        self.centros_salud = []
        self.cirujanos_esp = []
        self.cirujanos_gen = []
        self.vehiculos_terr = []
        self.aviones = []
        self.helic = []
        self.distancias_centros = {}
        self.organos = []


    def registrar_donante(self, donante):
        # Validar centro de salud
        if donante.centro not in self.centros_salud:
            print(f"\n❌ Centro de salud del donante {donante.nombre} no está registrado.")
            return
        
        # Validar DNI único entre donantes y receptores
        for d in self.donantes + self.receptores:
            if d.dni == donante.dni:
                print(f"\n❌ El DNI de {donante.nombre} ya está registrado en el sistema (donante o receptor).")
                return
        
        self.donantes.append(donante)
        print(f"\nDonante {donante.nombre} registrado.")

    def registrar_organo(self, organo):
        self.organos.append(organo)


    def registrar_receptor(self, receptor):
        # Validar centro de salud
        if receptor.centro not in self.centros_salud:
            print(f"\n❌ Centro de salud del receptor {receptor.nombre} no está registrado.")
            return

        # Validar DNI único entre donantes y receptores
        for d in self.donantes + self.receptores:
            if d.dni == receptor.dni:
                print(f"\n❌ El DNI de {receptor.nombre} ya está registrado en el sistema (donante o receptor).")
                return

        # Insertar receptor en orden de prioridad (mayor número = mayor prioridad)
        i = 0
        while i < len(self.receptores):
            actual = self.receptores[i]
            if receptor.prioridad() < actual.prioridad():
                i += 1
            elif receptor.prioridad() == actual.prioridad():
                fecha_nuevo = datetime.strptime(receptor.fecha_lista, "%d/%m/%Y")
                fecha_actual = datetime.strptime(actual.fecha_lista, "%d/%m/%Y")
                if fecha_nuevo > fecha_actual:
                    i += 1
                else:
                    break
            else:  # receptor.prioridad() > actual.prioridad()
                break

        self.receptores.insert(i, receptor)
        print(f"\n✅ Receptor {receptor.nombre} registrado en lista de espera (ordenado por prioridad).")


    def registrar_centro(self, centro):
        self.centros_salud.append(centro)
        print(f"\nCentro de salud {centro.nombre} registrado.")
        
        # Calcular y almacenar la distancia con otros centros registrados
        for otro_centro in self.centros_salud[:-1]:
            distancia = self.calcular_distancia_centros(centro, otro_centro)
            self.distancias_centros[(centro.nombre, otro_centro.nombre)] = distancia
            self.distancias_centros[(otro_centro.nombre, centro.nombre)] = distancia  

    def registrar_cirujano_esp(self, cirujano):
        self.cirujanos_esp.append(cirujano)
        print(f"\nCirujano especializado {cirujano.nombre} registrado.")

    def registrar_cirujano_gen(self, cirujano):
        self.cirujanos_gen.append(cirujano)
        print(f"\nCirujano general {cirujano.nombre} registrado.")

    def registrar_vehiculo_terr(self, vehiculo_terr):
        self.vehiculos_terr.append(vehiculo_terr)
        print(f"\nVehículo registrado")

    def registrar_avion(self, avion):
        self.aviones.append(avion)
        print(f"\nVehículo registrado")

    def registrar_helic(self, helic):
        self.helic.append(helic)
        print(f"\nVehículo registrado")

       
    def mostrar_estado(self):
        print("\n------------------ ESTADO ACTUAL DEL SISTEMA -------------------")
        print(f"Donantes registrados: {len(self.donantes)}")
        print(f"Receptores en lista de espera: {len(self.receptores)}")
        print(f"Centros de salud registrados: {len(self.centros_salud)}")
        print(f"Cirujanos especializados disponibles: {len(self.cirujanos_esp)}")
        print(f"Cirujanos generales disponibles: {len(self.cirujanos_gen)}")
        print(f"Vehículos terrestres: {len(self.vehiculos_terr)}")
        print(f"Aviones disponibles: {len(self.aviones)}")
        print(f"Helicópteros disponibles: {len(self.helic)}")
        print("------------------------------------------------------------------\n")

    def mostrar_lista_espera(self):
        print("\n--------------------------Lista de espera:---------------------------")
        for r in self.receptores:
            print(f"{r.nombre} - Órgano: {r.organo_r} - Fecha: {r.fecha_lista} ")
        print("-----------------------------------------------------------------------\n")

    def calcular_distancia_centros(self, centro1, centro2):
        coords_1 = (centro1.latitud, centro1.longitud)
        coords_2 = (centro2.latitud, centro2.longitud)
        return distance(coords_1, coords_2).km
    
    def cambiar_especialidad(self):
        for cirujano in self.cirujanos_esp:
            if cirujano.especialidad == "cardiovascular":
                cirujano.especialidad = ["corazon"]
            elif cirujano.especialidad == "pulmonar":
                cirujano.especialidad = ["pulmon"]
            elif cirujano.especialidad == "traumatologo":
                cirujano.especialidad = ["huesos"]
            elif cirujano.especialidad == "plastico":
                cirujano.especialidad = ["piel", "corneas"]
            elif cirujano.especialidad == "gastroenterologo":
                cirujano.especialidad = ["instestino", "rinion", "higado", "pancreas"]


    def obtener_numero_aleatorio(self):
        return random.randint(1, 10)

    def realizar_transplante(self, donante, receptor, indice):
        print(f"\n🩺 Transplante realizado entre Donante {donante.nombre} y Receptor {receptor.nombre}")
        self.receptores.remove(receptor)

        donante.organos_d.pop(indice)
        if not donante.organos_d:
            self.donantes.remove(donante)
    
    def ordenar_vehiterres(self, donante):
        n = len(self.vehiculos_terr)
        for i in range(n):
            for j in range(0, n - i - 1):
                v1 = self.vehiculos_terr[j]
                v2 = self.vehiculos_terr[j + 1]

                # Cálculo del valor velocidad / distancia
                d1 = self.calcular_distancia_centros(v1, donante.centro)
                d2 = self.calcular_distancia_centros(v2, donante.centro)
                
                #calculo trafico con random
                demora1=random.randint (0,60)/60
                demora2=random.randint (0,60)/60

                c1 = (d1 / v1.velocidad if v1.velocidad != 0 else float('inf')) + demora1
                c2 = (d2 / v2.velocidad if v2.velocidad != 0 else float('inf')) + demora2


                # Si el segundo es "mejor" (mayor velocidad/distancia), teniendo en cuenta el trafico, lo sube
                if c1 < c2:
                    self.vehiculos_terr[j], self.vehiculos_terr[j + 1] = self.vehiculos_terr[j + 1], self.vehiculos_terr[j]

    def transportar_organo(self, donante, receptor):
        centro_donante = donante.centro
        centro_receptor = receptor.centro
        clave = (centro_donante.nombre, centro_receptor.nombre)

        # Calcular distancia si aún no se había hecho
        if clave not in self.distancias_centros:
            distancia = self.calcular_distancia_centros(centro_donante, centro_receptor)
            self.distancias_centros[clave] = distancia
            self.distancias_centros[(centro_receptor.nombre, centro_donante.nombre)] = distancia

        distancia = self.distancias_centros[clave]
        print(f"\n📍 Distancia entre centros: {distancia:.2f} km")

        # 🔹 Transporte asignado por el centro del donante
        if centro_donante.provincia != centro_receptor.provincia:
            print("\n✈️ Transporte requerido: AVIÓN")
            if self.aviones:
                print("\nAvión asignado con éxito.")
                return True
            else:
                print("\n❌ No hay aviones disponibles.")
                return False

        elif centro_donante.partido != centro_receptor.partido:
            print("\n🚁 Transporte requerido: HELICÓPTERO")
            if self.helic:
                print("\nHelicóptero asignado con éxito.")
                return True
            else:
                print("\n❌ No hay helicópteros disponibles.")
                return False

        else:
            print("\n🚑 Transporte requerido: VEHÍCULO TERRESTRE")
            self.ordenar_vehiterres(donante)
            if self.vehiculos_terr:
                print(f"\nvelocidad : {self.vehiculos_terr[0].velocidad}")
                longitud = centro_donante.longitud
                latitud = centro_donante.latitud
                long1 = centro_receptor.longitud
                lat2 = centro_receptor.latitud
                print(f"\nVehículo terrestre asignado con exito")
                print("\nyendo a buscar el organo")
                self.vehiculos_terr[0].actualizar_ubicacion(longitud, latitud)
                print("\nyendo a dejar el organo")
                self.vehiculos_terr[0].actualizar_ubicacion(long1, lat2)
                return True
            else:
                print("\n❌ No hay vehículos terrestres disponibles.")
                return False

    def encontrar_donante_compatible(self, receptor):
        for donante in self.donantes:
             for organo_d in donante.organos_d:
                if organo_d.nombre == receptor.organo_r and receptor.t_sangre == donante.t_sangre:
                    return donante
        return None
    
    def indice(self, organo, lista_organos):
        n = len(lista_organos)
        for i in range (n):
            if lista_organos[i].nombre == organo:
                return i
    
    def centro_con_cirujanos(self, centro):
        hay_gen = any(c.centro == centro for c in self.cirujanos_gen)
        hay_esp = any(c.centro == centro for c in self.cirujanos_esp)
        return hay_gen or hay_esp
    
    def evaluar_operacion(self, centro, organo: Organo, indice):
        ahora = datetime.now()
        horas_desde_ablacion = int((ahora - organo[indice].ablacion).total_seconds() // 3600)

        organo_apto = horas_desde_ablacion <= 20
        cirujano_disponible = False

        # Verificar cirujanos especialistas
        cirujanos_esp_en_centro = [c for c in self.cirujanos_esp if c.centro == centro]

        for cirujano in cirujanos_esp_en_centro:
            if organo[indice].nombre in cirujano.especialidad and cirujano.operaciones_realizadas_hoy == 0:
                cirujano_disponible = True
                if organo_apto:
                    if self.obtener_numero_aleatorio() >= 3:
                        cirujano.operaciones_realizadas_hoy = 1
                        print(f"\nLa operación la realiza el cirujano especialista {cirujano.nombre} (mayor probabilidad de que salga bien)")
                        return True
                    else:
                        print("La operación falló")
                        return False

        # Verificar cirujanos generales
        cirujanos_gen_en_centro = [c for c in self.cirujanos_gen if c.centro == centro]

        for cirujano in cirujanos_gen_en_centro:
            if cirujano.operaciones_realizadas_hoy == 0:
                cirujano_disponible = True
                if organo_apto:
                    if self.obtener_numero_aleatorio() > 5:
                        cirujano.operaciones_realizadas_hoy = 1
                        print(f"\nLa operación la realiza el cirujano general {cirujano.nombre} (menor probabilidad de que salga bien)")
                        return True
                    else:
                        print("La operación falló")
                        return False

        # Mensajes finales (solo si no se pudo operar)
        if not cirujano_disponible:
            print("\nNo se puede realizar la operación porque todos los cirujanos ya operaron hoy.")
        if not organo_apto:
            print("\nNo se puede realizar la operación porque el órgano tiene más de 20 horas desde la ablación.")
        
        return False

        

    def match(self):
        self.cambiar_especialidad()
        matches_realizados = False
        i = 0
        while i < len(self.receptores):
            receptor = self.receptores[i]
            print(f"\nchequeando receptor {receptor.nombre}")
            
            if not self.centro_con_cirujanos(receptor.centro):
                print(f"\n❌ No hay cirujanos disponibles en el centro de salud de {receptor.nombre}. Operación cancelada.")
                i += 1
                continue
                
            donante = self.encontrar_donante_compatible(receptor)
            if not donante:
                i += 1
                continue
                
            print(f"\n✔️ Match entre Receptor {receptor.nombre} y Donante {donante.nombre}")
            indice_organo = self.indice(receptor.organo_r, donante.organos_d)
            
            if donante.centro != receptor.centro and not self.transportar_organo(donante, receptor):
                print("\n🚫 No se pudo transportar el órgano. Match cancelado.")
                i += 1
                continue
                
            if self.evaluar_operacion(receptor.centro, donante.organos_d, indice_organo):
                print("\n✅ Operación exitosa")
                self.realizar_transplante(donante, receptor, indice_organo)
                matches_realizados = True
                # No incrementamos i porque realizar_transplante ya eliminó al receptor
                # y ahora todos los elementos se desplazaron una posición 
                # El elemento que estaba en i+1 ahora está en i
            else:
                if 0 <= indice_organo < len(donante.organos_d):
                    donante.organos_d.pop(indice_organo)
                    if not donante.organos_d:
                        self.donantes.remove(donante)
                
                # Reinsertamos el receptor al inicio para considerarlo nuevamente
                self.receptores.pop(i)
                self.receptores.insert(0, receptor)
                self.mostrar_lista_espera()
                i = 0  # Reiniciamos el índice para comenzar desde el principio
                continue
                
        
            
        if not matches_realizados:
            print("\n❌ No hubo match disponible.")