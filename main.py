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

    #incucai.match()
    #print(incucai)
    #incucai.mostrar_lista_espera()


if __name__ == "__main__":
    main()
