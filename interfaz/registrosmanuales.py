import tkinter as tk
from tkinter import ttk, messagebox

from sistema.match import Match
from .registroreceptor import RegistroReceptorApp
from .registrodonante import RegistroDonanteApp
from .registrodonantevivo import RegistroDonanteVivoApp
from .salida_metodos import SalidaMetodos
from .ventana import Ventana
from .estado_incucai import EstadoIncucai
from .mostrar_match import MostrarMatch
from .lista_centros import ListaCentros
from .posicion_lista import PosicionLista


class IncucaiApp:

    def __init__(self, root, incucai):
        self.root = root
        self.incucai = incucai
        self._ventana_principal()
        self._interfaz_principal()

    def _ventana_principal(self):
        """Configura la ventana principal"""
        self.root.title("🏥 Sistema INCUCAI - Gestión de Trasplantes")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#ecf0f1")
        width, height = map(int, "900x700".split("x"))
        Ventana.centrar_ventana(self.root, width, height)

    def _interfaz_principal(self):
        """Crea la interfaz principal"""
        main_frame = ttk.Frame(self.root, padding=30, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._encabezado(main_frame)
        self._descripcion(main_frame)
        self._botones(main_frame)

    def _encabezado(self, parent):
        """Crea el encabezado de la aplicación"""
        ttk.Label(
            parent, text="🏥 Sistema de Gestión INCUCAI", style="Header.TLabel"
        ).pack(pady=(0, 20))

    def _descripcion(self, parent):
        """Crea la descripción de la aplicación"""
        description = (
            "Sistema integral para la gestión de donantes, receptores\n"
            "y coordinación de trasplantes de órganos"
        )

        ttk.Label(
            parent,
            text=description,
            wraplength=500,
            justify="center",
            style="Info.TLabel",
        ).pack(pady=(0, 30))

    def _botones(self, parent):
        """Crea los botones de acción principales"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, expand=True)

        buttons_config = [
            (" Estado Actual", self._mostrar_str_incucai, "Primary.TButton"),
            (" Registrar Receptor", self._registro_receptor, "TButton"),
            (" Registrar Donante", self._registro_donante, "TButton"),
            (" Registrar Donante Vivo", self._registro_donante_vivo, "TButton"),
            (" Realizar Match", self._realizar_match, "TButton"),
            (
                " Ver lista de espera de un centro",
                self._mostrar_lista_espera_centro,
                "TButton",
            ),
            (
                " Ver posicion de receptor en lista de espera",
                self._mostrar_posicion_receptor_espera,
                "TButton",
            ),
        ]

        for text, command, style in buttons_config:
            ttk.Button(
                button_frame, text=text, command=command, width=30, style=style
            ).pack(pady=8)

    # Métodos para abrir formularios

    def _mostrar_str_incucai(self):  # boton 1
        """
        Método para mostrar el __str__ de INCUCAI en una ventana emergente
        """
        try:
            str_incucai = str(self.incucai)
            EstadoIncucai.mostrar_str(self, str_incucai)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al mostrar información de INCUCAI: {e}"
            )

    def _mostrar_posicion_receptor_espera(self):
        """
        Método para manejar el botón 'Ver posición de receptor en lista de espera'
        Permite seleccionar un receptor y ver su posición en la lista de espera
        """
        try:
            # Obtener lista de receptores disponibles
            receptores = self.incucai.receptores  # Asumiendo que existe este método

            if not receptores:
                messagebox.showwarning(
                    "Sin receptores", "No hay receptores registrados."
                )
                return

            # Crear ventana para seleccionar receptor
            receptor_seleccionado = PosicionLista.seleccionar_receptor(self, receptores)

            if receptor_seleccionado:
                # Capturar la salida del método de INCUCAI
                salida_capturada = PosicionLista.capturar_salida_prioridad(self,
                    receptor_seleccionado
                )

                # Mostrar la salida en ventana emergente
                PosicionLista.mostrar_posicion(self, salida_capturada)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al consultar posición del receptor: {e}"
            )

    def _mostrar_lista_espera_centro(self):
        """
        Método para manejar el botón 'Mostrar lista de espera de un centro'
        Muestra ventanas emergentes para seleccionar centro y ver receptores
        """
        try:
            # Obtener lista de centros disponibles
            centros = self.incucai.centros_salud

            if not centros:
                messagebox.showwarning(
                    "Sin centros", "No hay centros de salud registrados."
                )
                return

            # Crear ventana para seleccionar centro
            centro_seleccionado = ListaCentros.seleccionar_centro(self, centros)

            if centro_seleccionado:
                # Capturar la salida del método de INCUCAI
                salida_capturada = ListaCentros.capturar_salida_incucai(self,
                    centro_seleccionado
                )

                # Mostrar la salida en ventana emergente
                ListaCentros.mostrar_salida(self, salida_capturada)

        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la lista de espera: {e}")

    def _realizar_match(self):
        """Ejecuta el algoritmo de matching y muestra resultados"""
        with SalidaMetodos() as capture:
            try:
                match_instance = Match(self.incucai)
                match_instance.match()
            except Exception as e:
                print(f"Error en el proceso de matching: {str(e)}")

        resultado = capture.get_output()
        MostrarMatch.mostrar_match(self, resultado)

    def _registro_receptor(self):
        """Abre el formulario de registro de receptor"""
        receptor_window = tk.Toplevel(self.root)
        RegistroReceptorApp(receptor_window, self.incucai)
        receptor_window.transient(self.root)

    def _registro_donante(self):
        """Abre el formulario de registro de donante"""
        donante_window = tk.Toplevel(self.root)
        RegistroDonanteApp(donante_window, self.incucai)
        donante_window.transient(self.root)

    def _registro_donante_vivo(self):
        """Abre el formulario de registro de donante vivo"""
        donante_vivo_window = tk.Toplevel(self.root)
        RegistroDonanteVivoApp(donante_vivo_window, self.incucai)
        donante_vivo_window.transient(self.root)
