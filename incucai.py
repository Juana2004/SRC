from datetime import datetime
import random
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="mi_aplicacion")
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

        # Insertar receptor en orden de prioridad
        i = 0
        if self.receptores == []:
            self.receptores.insert(i, receptor)
        else:
            while i < len(self.receptores):
                actual = self.receptores[i]
                if receptor.prioridad() < actual.prioridad():
                    break
                elif receptor.prioridad() == actual.prioridad():
                    fecha_nuevo = datetime.strptime(receptor.fecha_lista, "%d/%m/%Y")
                    fecha_actual = datetime.strptime(actual.fecha_lista, "%d/%m/%Y")
                    if fecha_nuevo < fecha_actual:
                        break
                i += 1
            self.receptores.insert(i, receptor)

        print(f"\nReceptor {receptor.nombre} registrado en lista de espera (ordenado por prioridad).")


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
        print("\n--- ESTADO ACTUAL DEL SISTEMA ---")
        print(f"Donantes registrados: {len(self.donantes)}")
        print(f"Receptores en lista de espera: {len(self.receptores)}")
        print(f"Centros de salud registrados: {len(self.centros_salud)}")
        print(f"Cirujanos especializados disponibles: {len(self.cirujanos_esp)}")
        print(f"Cirujanos generales disponibles: {len(self.cirujanos_gen)}")
        print(f"Vehículos terrestres: {len(self.vehiculos_terr)}")
        print(f"Aviones disponibles: {len(self.aviones)}")
        print(f"Helicópteros disponibles: {len(self.helic)}")
        print("----------------------------------\n")

    def mostrar_lista_espera(self):
        print("\nLista de espera:")
        for r in self.receptores:
            print(f"{r.nombre} - Órgano: {r.organo_r} - Fecha: {r.fecha_lista} - Estado: {r.estado}")

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

    def realizar_transplante(self, donante, receptor):
        print(f"\n🩺 Transplante realizado entre Donante {donante.nombre} y Receptor {receptor.nombre}")
        self.receptores.remove(receptor)
        self.donantes.remove(donante)

    def centro_con_cirujanos(self, centro):
        hay_gen = any(c.centro == centro for c in self.cirujanos_gen)
        hay_esp = any(c.centro == centro for c in self.cirujanos_esp)
        return hay_gen or hay_esp
    
    def evaluar_operacion(self, centro, organo: Organo):
        ahora = datetime.now()
        resta = int((ahora - organo[0].ablacion).total_seconds() // 3600)

        print(resta)
        # Intentar primero con cirujano especialista
        for cirujano in self.cirujanos_esp:
            if cirujano.centro == centro and organo[0].nombre in cirujano.especialidad:
                if self.obtener_numero_aleatorio() >= 3 and resta<= 20:
                    return True

        # Si no fue posible con especialista, intentar con cualquier cirujano del centro
        for cirujano in self.cirujanos_gen:
            if cirujano.centro == centro:
                if self.obtener_numero_aleatorio() > 5 and resta <= 20:
                    return True

        return False


    def encontrar_donante_compatible(self, receptor):
        for donante in self.donantes:
             for organo_d in donante.organos_d:
                if organo_d.nombre == receptor.organo_r and receptor.t_sangre == donante.t_sangre:
                    return donante
        return None
    
    def ordenar_vehiterres(self, donante):
        n = len(self.vehiculos_terr)
        for i in range(n):
            for j in range(0, n - i - 1):
                v1 = self.vehiculos_terr[j]
                v2 = self.vehiculos_terr[j + 1]

                # Cálculo del valor velocidad / distancia
                d1 = self.calcular_distancia_centros(v1, donante.centro)
                d2 = self.calcular_distancia_centros(v2, donante.centro)

                c1 = v1.velocidad / d1 if d1 != 0 else float('inf')
                c2 = v2.velocidad / d2 if d2 != 0 else float('inf')

                # Si el segundo es "mejor" (mayor velocidad/distancia), lo sube
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
        print(f"📍 Distancia entre centros: {distancia:.2f} km")

        # 🔹 Transporte asignado por el centro del donante
        if centro_donante.provincia != centro_receptor.provincia:
            print("✈️ Transporte requerido: AVIÓN")
            if self.aviones:
                print("Avión asignado con éxito.")
                return True
            else:
                print("❌ No hay aviones disponibles.")
                return False

        elif centro_donante.partido != centro_receptor.partido:
            print("🚁 Transporte requerido: HELICÓPTERO")
            if self.helic:
                print("Helicóptero asignado con éxito.")
                return True
            else:
                print("❌ No hay helicópteros disponibles.")
                return False

        else:
            print("🚑 Transporte requerido: VEHÍCULO TERRESTRE")
            self.ordenar_vehiterres(donante)
            if self.vehiculos_terr:
                print(f"velocidad : {self.vehiculos_terr[0].velocidad}")
                longitud = centro_donante.longitud
                latitud = centro_donante.latitud
                long1 = centro_receptor.longitud
                lat2 = centro_receptor.latitud
                print(f"Vehículo terrestre asignado con exito")
                print("yendo a buscar el organo")
                self.vehiculos_terr[0].actualizar_ubicacion(longitud, latitud)
                print("yendo a dejar el organo")
                self.vehiculos_terr[0].actualizar_ubicacion(long1, lat2)
                return True
            else:
                print("❌ No hay vehículos terrestres disponibles.")
                return False



    def match(self):
        self.cambiar_especialidad()
        matches_realizados = False
        receptores_a_evaluar = self.receptores[:]

        for receptor in receptores_a_evaluar:
            if not self.centro_con_cirujanos(receptor.centro):
                print(f"❌ No hay cirujanos disponibles en el centro de salud de {receptor.nombre}. Operación cancelada.")
                continue

            donante = self.encontrar_donante_compatible(receptor)
            if not donante:
                continue

            print(f"\n✔️ Match entre Receptor {receptor.nombre} y Donante {donante.nombre}")

            if donante.centro != receptor.centro and not self.transportar_organo(donante, receptor):
                print("🚫 No se pudo transportar el órgano. Match cancelado.")
                continue

            if self.evaluar_operacion(receptor.centro, donante.organos_d):
            
                print("✅ Operación exitosa")
                self.realizar_transplante(donante, receptor)
                matches_realizados = True
            else:
                print("Fallo la operacion")
                self.donantes.remove(donante)

        if not matches_realizados:
            print("\n❌ No hubo match disponible.")

