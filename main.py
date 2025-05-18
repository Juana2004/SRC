import sys
import os
sys.path.append(os.path.dirname(__file__))
#garantiza que Python pueda resolver correctamente los imports relativos desde el directorio raíz del proyecto.

from registros import Registros, RegistroReceptorApp
from incucai import INCUCAI
import tkinter as tk

def main():
    incucai = INCUCAI()
    registro =Registros()
    
    registro.Registrar(incucai)#lo que cambie para que anden los centros

    root = tk.Tk()
    app = RegistroReceptorApp(root, incucai)
    root.mainloop()

    incucai.match()
    incucai.mostrar_estado()

if __name__ == "__main__":
    main()
