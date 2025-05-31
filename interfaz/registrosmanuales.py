import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import io
import sys
from io import StringIO

from sistema.match import Match
from .registroreceptor import RegistroReceptorApp
from .registrodonante import RegistroDonanteApp
from .registrodonantevivo import RegistroDonanteVivoApp
from .formato_lista import FormatoListaDeEspera
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

        self._setup_main_window()
        self._create_main_interface()

    def _setup_main_window(self):
        """Configura la ventana principal"""
        self.root.title("🏥 Sistema INCUCAI - Gestión de Trasplantes")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#ecf0f1")

        # Centrar ventana
        width, height = map(int, "900x700".split("x"))
        Ventana.centrar_ventana(self.root, width, height)

    def _create_main_interface(self):
        """Crea la interfaz principal"""
        main_frame = ttk.Frame(self.root, padding=30, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._create_header(main_frame)
        self._create_description(main_frame)
        self._create_action_buttons(main_frame)

    def _create_header(self, parent):
        """Crea el encabezado de la aplicación"""
        ttk.Label(
            parent, text="🏥 Sistema de Gestión INCUCAI", style="Header.TLabel"
        ).pack(pady=(0, 20))

    def _create_description(self, parent):
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

    def _create_action_buttons(self, parent):
        """Crea los botones de acción principales"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, expand=True)

        buttons_config = [
            (" Estado Actual", self.mostrar_str_incucai, "Primary.TButton"),
            (" Registrar Receptor", self.open_receptor_form, "TButton"),
            (" Registrar Donante", self.open_donante_form, "TButton"),
            (" Registrar Donante Vivo", self.open_donante_vivo_form, "TButton"),
            (" Realizar Match", self.realizar_match, "TButton"),
            (
                " Ver lista de espera de un centro",
                self.mostrar_lista_espera_centro,
                "TButton",
            ),
            (
                " Ver posicion de receptor en lista de espera",
                self.mostrar_posicion_receptor_espera,
                "TButton",
            ),
        ]

        for text, command, style in buttons_config:
            ttk.Button(
                button_frame, text=text, command=command, width=30, style=style
            ).pack(pady=8)

    # Métodos para abrir formularios

    def mostrar_str_incucai(self):  # boton 1
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

    def mostrar_posicion_receptor_espera(self):
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

    def mostrar_lista_espera_centro(self):
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

    def realizar_match(self):
        """Ejecuta el algoritmo de matching y muestra resultados"""
        with SalidaMetodos() as capture:
            try:
                match_instance = Match(self.incucai)
                match_instance.match()
            except Exception as e:
                print(f"Error en el proceso de matching: {str(e)}")

        resultado = capture.get_output()
        MostrarMatch.mostrar_match(self, resultado)

    def open_receptor_form(self):
        """Abre el formulario de registro de receptor"""
        receptor_window = tk.Toplevel(self.root)
        RegistroReceptorApp(receptor_window, self.incucai)
        receptor_window.transient(self.root)

    def open_donante_form(self):
        """Abre el formulario de registro de donante"""
        donante_window = tk.Toplevel(self.root)
        RegistroDonanteApp(donante_window, self.incucai)
        donante_window.transient(self.root)

    def open_donante_vivo_form(self):
        """Abre el formulario de registro de donante vivo"""
        donante_vivo_window = tk.Toplevel(self.root)
        RegistroDonanteVivoApp(donante_vivo_window, self.incucai)
        donante_vivo_window.transient(self.root)
