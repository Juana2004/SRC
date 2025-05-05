from datetime import datetime
import random
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="mi_aplicacion")
from geopy.distance import geodesic

class INCUCAI:

    def __init__(self):
        self.donantes = []
        self.receptores = []
        self.centros_salud = []
        self.organismos = []
        self.cirujanos = []
        self.vehiculos_terr = []
        self.aviones = []
        self.helic = []


    def registrar_donante(self, donante):
        for don in self.donantes:
            if don.dni == donante.dni:
                print("No se puede repetir DNI")
                return  # Salir sin registrar

        self.donantes.append(donante)
        print(f"\nDonante {donante.nombre} registrado.")


    def registrar_receptor(self, receptor):
        i = 0
        if self.receptores == []:
            self.receptores.insert(i, receptor)
            print(f"Receptor {receptor.nombre} registrado en lista de espera (ordenado por prioridad).")
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
            print(f"Receptor {receptor.nombre} registrado en lista de espera (ordenado por prioridad).")

    def registrar_centro(self, centro):
        self.centros_salud.append(centro)
        print(f"Centro de salud {centro.nombre} registrado.")

    def registrar_cirujano(self, cirujano):
        self.cirujanos.append(cirujano)
        print(f"Cirujano {cirujano.nombre} registrado.")

    
    def cambiar_especialidad(self):
        for cirujano in self.cirujanos:
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
            

    def registrar_vehiculo_terr(self, vehiculo_terr):
        self.vehiculos_terr.append(vehiculo_terr)
    
    def registrar_avion(self, avion):
        self.aviones.append(avion)

    def registrar_helic(self, helic):
        self.helic.append(helic)
       
    def mostrar_estado(self):
        print("\n--- ESTADO ACTUAL DEL SISTEMA ---")
        print(f"Donantes registrados: {len(self.donantes)}")
        print(f"Receptores en lista de espera: {len(self.receptores)}")
        print(f"Centros de salud registrados: {len(self.centros_salud)}")
        print(f"Cirujanos disponibles: {len(self.cirujanos)}")
        print(f"Vehículos terrestres: {len(self.vehiculos_terr)}")
        print(f"Aviones disponibles: {len(self.aviones)}")
        print(f"Helicópteros disponibles: {len(self.helic)}")

        print("----------------------------------\n")

    def mostrar_lista_espera(self):
        print("\nLista de espera:")
        for r in self.receptores:
            print(f"{r.nombre} - Órgano: {r.organo_r} - Fecha: {r.fecha_lista} - Estado: {r.estado}")


    def obtener_numero_aleatorio(self):
        return random.randint(1, 10)

    def realizar_transplante(self, donante, receptor):
        print(f"\n🩺 Transplante realizado entre Donante {donante.nombre} y Receptor {receptor.nombre}")
        self.receptores.remove(receptor)
        donante.organos_d.remove(receptor.organo_r)
        if not donante.organos_d:
            self.donantes.remove(donante)

    def match(self):
        self.cambiar_especialidad()
        matches_realizados = False
        receptores_a_evaluar = self.receptores[:]

        for receptor in receptores_a_evaluar:
            for donante in self.donantes:
                if receptor.organo_r in donante.organos_d and receptor.tipo_sangre == donante.tipo_sangre:
                    print(f"\n✔️ Match entre Receptor {receptor.nombre} y Donante {donante.nombre}")
                    centro_receptor = receptor.centro
                    centro_donante = donante.centro
                    organo = receptor.organo_r

                    if centro_receptor != centro_donante:
                        if not self.transportar_organo(donante, receptor):
                            print("🚫 No se pudo transportar el órgano. Match cancelado.")
                            continue  # Pasar al siguiente donante

                    if self.evaluar_operacion(centro_receptor, organo):
                        print("✅ Operación exitosa")
                        self.realizar_transplante(donante, receptor)
                        matches_realizados = True
                    else:
                        print("⚠️ Falló la operación")
                        self.donantes.remove(donante)

                    break  # Solo un donante por receptor

        if not matches_realizados:
            print("\n❌ No hubo match disponible.")

    def evaluar_operacion(self, centro, organo):
        # Intentar primero con cirujano especialista
        for cirujano in self.cirujanos:
            if cirujano.centro == centro and organo in cirujano.especialidad:
                if self.obtener_numero_aleatorio() >= 3:
                    return True

        # Si no fue posible con especialista, intentar con cualquier cirujano del centro
        for cirujano in self.cirujanos:
            if cirujano.centro == centro:
                if self.obtener_numero_aleatorio() > 5:
                    return True

        return False
    
    from geopy.distance import geodesic  # Asegúrate de importar esto

    # Método para calcular la distancia entre dos direcciones
    def calcular_distancia(self, direccion1, direccion2):
        ubicacion1 = geolocator.geocode(direccion1)
        ubicacion2 = geolocator.geocode(direccion2)

        if not ubicacion1 or not ubicacion2:
            print(f"No se pudo obtener la ubicación de: {direccion1} o {direccion2}")
            return None

        coord1 = (ubicacion1.latitude, ubicacion1.longitude)
        coord2 = (ubicacion2.latitude, ubicacion2.longitude)
        return geodesic(coord1, coord2).kilometers
    
    def transportar_organo(self, donante, receptor):
        dir_don = donante.centro.direccion
        dir_rec = receptor.centro.direccion
        prov_don = donante.centro.provincia
        prov_rec = receptor.centro.provincia
        partido_don = donante.centro.partido
        partido_rec = receptor.centro.partido

        distancia = self.calcular_distancia(dir_don, dir_rec)
        if distancia is None:
            return False

        print(f"Distancia entre centros: {distancia:.2f} km")

        if prov_don != prov_rec:
            print("✈️ Transporte requerido: AVIÓN")
            if self.aviones:
                print("Avión asignado con éxito.")
                return True
            else:
                print("❌ No hay aviones disponibles.")
                return False

        elif partido_don != partido_rec:
            print("🚁 Transporte requerido: HELICÓPTERO")
            if self.helic:
                print("Helicóptero asignado con éxito.")
                return True
            else:
                print("❌ No hay helicópteros disponibles.")
                return False

        else:
            print("🚑 Transporte requerido: VEHÍCULO TERRESTRE")
            if self.vehiculos_terr:
                print("Vehículo terrestre asignado con éxito.")
                return True
            else:
                print("❌ No hay vehículos terrestres disponibles.")
                return False


   