from registros.registros import Registros
from registros.registrosmanuales import IncucaiApp
from sistema.incucai import INCUCAI
import tkinter as tk

def main():
    incucai = INCUCAI()
    registro =Registros()
    registro.Registrar(incucai)
    
    root = tk.Tk()
    app = IncucaiApp(root, incucai)
    root.mainloop()

    print(incucai)


if __name__ == "__main__":
    main()
