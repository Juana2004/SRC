import tkinter as tk
from abc import ABC

class Ventana(ABC):
    """
    Clase abstracta para gestionar ventanas en Tkinter
    """

    def __init__(self):
        # Constructor de la clase. Lanza un error si se intenta instanciar directamente.
        if type(self) is Ventana:
            raise TypeError("Ventana es una clase abstracta y no puede ser instanciada directamente.")
        super().__init__()

    @staticmethod
    def centrar_ventana(ventana, ancho, alto):
        """
        Método estático.
        Centra una ventana en el medio de la pantalla según el tamaño especificado.

        Parámetros:
        - ventana: la instancia de ventana de Tkinter
        - ancho: ancho deseado 
        - alto: alto deseado 
        """
        ventana.update_idletasks()  # Actualiza la geometría antes de calcular las posiciones
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)

        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    @staticmethod
    def crear_ventana_modal(padre, titulo, tamaño):
        """
        Método estático.
        Crea una ventana modal (bloquea la interacción con la ventana principal hasta que se cierre).

        Parámetros:
        - padre: la ventana padre sobre la cual se va a crear la modal
        - titulo: el título que va a tener la ventana modal
        - tamaño: string con el tamaño en formato 'ancho x alto' (por ejemplo, '400x300')

        Retorna:
        - La ventana modal (tk.Toplevel)
        """
        ventana = tk.Toplevel(padre)           # Crea una nueva ventana secundaria
        ventana.title(titulo)                  # Asigna el título
        ventana.transient(padre)              # Hace que esté asociada a la ventana padre
        ventana.grab_set()                    # Bloquea la interacción con la ventana principal
        ventana.resizable(True, True)         # Permite cambiar el tamaño

        ancho, alto = map(int, tamaño.split('x'))
        Ventana.centrar_ventana(ventana, ancho, alto)  

        return ventana
