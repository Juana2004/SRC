from sistema.transporte import Transporte
from sistema.gestor_cirujanos import GestorCirujanos
from sistema.gestor_donaciones import GestorDonaciones

class Match:
    def __init__(self, incucai):
        self.incucai = incucai
        self.transporte: object = Transporte(incucai)
        self.gestor_cirujanos: object = GestorCirujanos(incucai)
        self.gestor_donaciones: object = GestorDonaciones(incucai)

    def match(self):
        self.gestor_cirujanos.normalizar_especialidades()
        matches_realizados = False
        receptores_procesados = set()
        receptores_pendientes = list(self.incucai.receptores)
        
        while receptores_pendientes:
            receptor = receptores_pendientes.pop(0)
            receptor_id = id(receptor)
            print(f"\nEvaluando receptor: {receptor.nombre}\n")
            
            if not self.gestor_cirujanos.hay_cirujanos_en_centro(receptor.centro):
                print(f"\n❌ No hay cirujanos disponibles en el centro de {receptor.nombre}\n")
                continue
            
            # Obtener todos los donantes compatibles
            todos_donantes_compatibles = self.gestor_donaciones.compatibilidad(receptor)
            
            if not todos_donantes_compatibles:
                print(f"\n❌ No se encontró donante compatible para {receptor.nombre}\n")
                continue
    
            match_encontrado = False
            for donante, indice_organo in todos_donantes_compatibles:
    
                cirujanos_disponibles_ablacion = self.gestor_cirujanos.cirujanos_disponibles_ablacion(donante)

                if not cirujanos_disponibles_ablacion:
                    print(f"⚠️ No hay cirujanos disponibles para ablación del donante {donante.nombre}. Probando siguiente donante...")
                    continue

                
                vehiculos_en_centro = self.transporte.vehiculo_en_centro(donante.centro, receptor.centro)
                if donante.centro != receptor.centro and not vehiculos_en_centro:
                    print(f"⚠️ No hay vehiculos disponibles para transporte desde {donante.centro} a {receptor.centro}. Probando siguiente donante...")
                    continue  
                
                print(f"✅ Match encontrado: {receptor.nombre} ↔ {donante.nombre}")

                print("\nSe inicia proceso de ablacion\n")
                self.gestor_cirujanos.realizar_operacion_ablacion(cirujanos_disponibles_ablacion[0])
                self.gestor_donaciones.registrar_ablacion_donante_vivo(donante, receptor.organo_receptor)
                
                exito_transporte, tiempo_transporte = self.gestionar_transporte(donante, receptor)

                if not exito_transporte:
                    continue 
                
                if self._ejecutar_operacion(donante, receptor, indice_organo, tiempo_transporte):
                    matches_realizados = True
                    receptores_procesados.add(receptor_id)
                    match_encontrado = True
                    break  # Match exitoso, pasar al siguiente receptor
                else:
                    self._manejar_operacion_fallida(
                        donante, receptor, indice_organo, receptores_pendientes
                    )
                    # Continuar con el siguiente donante si la operación falló
            
            if not match_encontrado:
                print(f"\n❌ No se pudo realizar match para {receptor.nombre} con ningún donante disponible\n")
        
        return matches_realizados

    def gestionar_transporte(self, donante, receptor) -> tuple[bool, float]:
        if donante.centro != receptor.centro:
            exito, tiempo = self.transporte.asignar_vehiculo(donante, receptor)
            if not exito:
                print("❌ No se pudo transportar el órgano. Match cancelado.")
                return False, 0.0
            else:
                return True, tiempo
        else:
            print("✅ Donante y receptor en el mismo centro. No se requiere transporte.")
            return True, 0.0 

    def _ejecutar_operacion(self, donante, receptor, indice_organo, tiempo_transporte):
        if self.gestor_cirujanos.evaluar_operacion(
            receptor.centro, donante.organos_donante[indice_organo], receptor, tiempo_transporte):
            print("✅ Operación exitosa")
            self.realizar_transplante(donante, receptor, indice_organo)
            return True
        return False

    def _manejar_operacion_fallida(self, donante, receptor, indice_organo, receptores_pendientes):
        centro_donante = donante.centro
        if 0 <= indice_organo < len(donante.organos_donante):
            organo_fallido = donante.organos_donante.pop(indice_organo)
            print(
                f"❌ Órgano {organo_fallido.nombre} descartado después de operación fallida"
            )
            if not donante.organos_donante and donante in self.incucai.donantes:
                self.incucai.donantes.remove(donante)
                centro_donante.donantes.remove(donante)
                print(f"🗑️ Donante {donante.nombre} removido del sistema (sin órganos disponibles)")
        if receptor in self.incucai.receptores:
            self.incucai.receptores.remove(receptor)
        receptores_pendientes.insert(0, receptor)
    
    def realizar_transplante(self, donante, receptor, indice_organo):
        print(
            f"Trasplante entre {donante.nombre} y {receptor.nombre} realizado con éxito"
        )
        centro_receptor = receptor.centro
        centro_donante = donante.centro
        self.incucai.receptores.remove(receptor)
        centro_receptor.receptores.remove(receptor)
        if 0 <= indice_organo < len(donante.organos_donante):
            donante.organos_donante.pop(indice_organo)
            if not donante.organos_donante and donante in self.incucai.donantes:
                self.incucai.donantes.remove(donante)
                centro_donante.donantes.remove(donante)
                print(f"🗑️ Donante {donante.nombre} removido del sistema.")