from registros.registros import Registros
from interfaz.registrosmanuales import IncucaiApp
from sistema.incucai import INCUCAI
import tkinter as tk
from sistema.match import Match

'''
En caso de querer ver por consola descomentar a match.match() y comentar 
root = tk.Tk()
app = IncucaiApp(root, incucai)
root.mainloop()
'''

def main():
    incucai = INCUCAI()
    registro =Registros()
    registro.Registrar(incucai)
    match = Match(incucai)
    #match.match()
    
    root = tk.Tk()
    app = IncucaiApp(root, incucai)
    root.mainloop()


if __name__ == "__main__":
    main()
