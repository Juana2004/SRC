from registros.registros import Registros
from interfaz.registrosmanuales import IncucaiApp
from sistema.incucai import INCUCAI
import tkinter as tk

def main():
    incucai = INCUCAI()
    registro =Registros()
    registro.Registrar(incucai)
    
    root = tk.Tk()
    app = IncucaiApp(root, incucai)
    root.mainloop()


if __name__ == "__main__":
    main()
