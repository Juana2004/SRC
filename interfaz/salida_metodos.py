import sys  # Módulo que permite acceder a la salida estándar del sistema
import io   # Módulo que permite trabajar con flujos de texto en memoria

class SalidaMetodos:
    """
    Clase que permite capturar todo lo que se imprime en la consola
    """

    def __init__(self):
        """
        Inicializa el buffer donde se va a guardar el texto y
        guarda una referencia al stdout original para poder restaurarlo después.
        """
        self.buffer = io.StringIO()         # Buffer de texto en memoria
        self.original_stdout = sys.stdout  # Guarda el stdout original

    def __enter__(self):
        """
        Método mágico
        Se ejecuta al entrar al bloque 'with'.
        Redirige la salida estándar (print) al buffer interno.
        """
        sys.stdout = self.buffer
        return self  # Devuelve la instancia para poder llamar a get_output()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Método mágico
        Se ejecuta al salir del bloque 'with'.
        Restaura la salida estándar al valor original.
        """
        sys.stdout = self.original_stdout

    def get_output(self) -> str:
        """
        Devuelve todo el texto capturado durante el uso del contexto.
        Returns:
            str: texto acumulado en el buffer.
        """
        return self.buffer.getvalue()
