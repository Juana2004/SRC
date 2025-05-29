import tkinter as tk
from tkinter import ttk
from sistema.match import Match
from registros.registroreceptor import RegistroReceptorApp
from registros.registrodonante import RegistroDonanteApp
from registros.registrodonantevivo import RegistroDonanteVivoApp
import io
import sys
 
class IncucaiApp:
    def __init__(self, root, incucai):
        self.root = root
        self.incucai = incucai
        self.root.title("Sistema INCUCAI")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.setup_styles()
        main_frame = ttk.Frame(root, padding=20, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(main_frame, text="Sistema de Gestión INCUCAI", style="Header.TLabel").pack(pady=(0, 40))
        ttk.Label(
            main_frame, 
            text="Seleccione una opción para registrar pacientes en el sistema", 
            wraplength=500,
            justify="center"
        ).pack(pady=(0, 30))
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, expand=True)
        ttk.Button(
            button_frame, 
            text="Registrar Receptor", 
            command=self.open_receptor_form,
            width=25,
            style="Accent.TButton"
        ).pack(pady=10)

        ttk.Button(
            button_frame, 
            text="Registrar Donante", 
            command=self.open_donante_form,
            width=25
        ).pack(pady=10)

        ttk.Button(
            button_frame, 
            text="Registrar Donante Vivo", 
            command=self.open_donante_vivo_form,
            width=25
        ).pack(pady=10)

        ttk.Button(
            button_frame,
            text="Realizar Match",
            command=self.realizar_match,
            width=25
        ).pack(pady=10)

    
    def setup_styles(self):
        '''
        Configura los estilos para los widgets de la interfaz
        '''

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", font=("Segoe UI", 11), background="#f2f2f2")
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TEntry", font=("Segoe UI", 11))

        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), background="#f2f2f2", foreground="#333")

        style.configure("Accent.TButton", foreground="white", background="#007acc")
        style.map("Accent.TButton",
                 background=[("active", "#005f99"), ("pressed", "#004c7a")])

        style.configure("Card.TFrame", background="white", relief="groove", borderwidth=1)
    
    def open_receptor_form(self):
        '''Crear una nueva ventana para el formulario de receptor'''
        receptor_window = tk.Toplevel(self.root)
        receptor_app = RegistroReceptorApp(receptor_window, self.incucai)
        receptor_window.transient(self.root)  # Hacer que la ventana sea dependiente de la principal
    
    def open_donante_form(self):
        '''Crear una nueva ventana para el formulario de donante'''
        donante_window = tk.Toplevel(self.root)
        donante_app = RegistroDonanteApp(donante_window, self.incucai)
        donante_window.transient(self.root)  # Hacer que la ventana sea dependiente de la principal
    
    def open_donante_vivo_form(self):
        '''Crear una nueva ventana para el formulario de donante vivo'''
        donante_vivo_window = tk.Toplevel(self.root)
        donante_vivo_app = RegistroDonanteVivoApp(donante_vivo_window, self.incucai)
        donante_vivo_window.transient(self.root)


    def realizar_match(self):
        buffer = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = buffer

        try:
            match_instance = Match(self.incucai)
            match_instance.match()
        finally:
            sys.stdout = sys_stdout_original

        resultado = buffer.getvalue()

        resultado_ventana = tk.Toplevel(self.root)
        resultado_ventana.title("Resultado del Match")
        resultado_ventana.geometry("500x400")
        resultado_ventana.transient(self.root)

        ttk.Label(resultado_ventana, text="Resultado del Match", style="Header.TLabel").pack(pady=(10, 5))

        text_box = tk.Text(resultado_ventana, wrap="word", font=("Courier", 10))
        text_box.pack(expand=True, fill="both", padx=10, pady=10)
        text_box.insert("1.0", resultado)
        text_box.configure(state="disabled")
