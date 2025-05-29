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
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.setup_styles()
        main_frame = ttk.Frame(root, padding=20, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(
            main_frame, text="Sistema de Gestión INCUCAI", style="Header.TLabel"
        ).pack(pady=(0, 40))
        ttk.Label(
            main_frame,
            text="Seleccione una opción para registrar pacientes en el sistema",
            wraplength=500,
            justify="center",
        ).pack(pady=(0, 30))
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, expand=True)
        ttk.Button(
            button_frame,
            text="Registrar Receptor",
            command=self.open_receptor_form,
            width=25,
            style="Accent.TButton",
        ).pack(pady=10)

        ttk.Button(
            button_frame,
            text="Registrar Donante",
            command=self.open_donante_form,
            width=25,
        ).pack(pady=10)

        ttk.Button(
            button_frame,
            text="Registrar Donante Vivo",
            command=self.open_donante_vivo_form,
            width=25,
        ).pack(pady=10)

        ttk.Button(
            button_frame, text="Realizar Match", command=self.realizar_match, width=25
        ).pack(pady=10)

        ttk.Button(
            button_frame,
            text="Mostrar lista de espera",
            command=self.mostrar_lista_de_espera,
            width=25,
        ).pack(pady=10)

    def setup_styles(self):
        """
        Configura los estilos para los widgets de la interfaz
        """

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", font=("Segoe UI", 11), background="#f2f2f2")
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TEntry", font=("Segoe UI", 11))

        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 20, "bold"),
            background="#f2f2f2",
            foreground="#333",
        )

        style.configure("Accent.TButton", foreground="white", background="#007acc")
        style.map(
            "Accent.TButton", background=[("active", "#005f99"), ("pressed", "#004c7a")]
        )

        style.configure(
            "Card.TFrame", background="white", relief="groove", borderwidth=1
        )

    def open_receptor_form(self):
        """Crear una nueva ventana para el formulario de receptor"""
        receptor_window = tk.Toplevel(self.root)
        receptor_app = RegistroReceptorApp(receptor_window, self.incucai)
        receptor_window.transient(
            self.root
        )  

    def open_donante_form(self):
        """Crear una nueva ventana para el formulario de donante"""
        donante_window = tk.Toplevel(self.root)
        donante_app = RegistroDonanteApp(donante_window, self.incucai)
        donante_window.transient(
            self.root
        ) 

    def open_donante_vivo_form(self):
        """Crear una nueva ventana para el formulario de donante vivo"""
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

        ttk.Label(
            resultado_ventana, text="Resultado del Match", style="Header.TLabel"
        ).pack(pady=(10, 5))

        text_box = tk.Text(resultado_ventana, wrap="word", font=("Courier", 10))
        text_box.pack(expand=True, fill="both", padx=10, pady=10)
        text_box.insert("1.0", resultado)
        text_box.configure(state="disabled")

    def mostrar_lista_de_espera(self):
        buffer = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = buffer
        try:
            self.incucai.mostrar_lista_de_espera()
        finally:
            sys.stdout = sys_stdout_original
        resultado = buffer.getvalue()
        
        resultado_ventana = tk.Toplevel(self.root)
        resultado_ventana.title("📋 Lista de Espera - INCUCAI")
        resultado_ventana.geometry("800x600")
        resultado_ventana.transient(self.root)
        resultado_ventana.grab_set()
        resultado_ventana.resizable(True, True)

        resultado_ventana.configure(bg='#f0f0f0')

        resultado_ventana.update_idletasks()
        x = (resultado_ventana.winfo_screenwidth() // 2) - (800 // 2)
        y = (resultado_ventana.winfo_screenheight() // 2) - (600 // 2)
        resultado_ventana.geometry(f"800x600+{x}+{y}")

        main_frame = ttk.Frame(resultado_ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
      
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(
            header_frame, 
            text="📋 Lista de Espera", 
            font=("Segoe UI", 16, "bold"),
            foreground="#2c3e50"
        ).pack(side="left")

        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", pady=(0, 10))
        
        lineas = [linea.strip() for linea in resultado.split('\n') if linea.strip()]
        total_pacientes = len([l for l in lineas if not l.startswith('-') and not l.startswith('=') and l])
        
        ttk.Label(
            info_frame,
            text=f"Total de pacientes en espera: {total_pacientes}",
            font=("Segoe UI", 10),
            foreground="#7f8c8d"
        ).pack(side="left")
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        ttk.Label(
            info_frame,
            text=f"Última actualización: {timestamp}",
            font=("Segoe UI", 10),
            foreground="#7f8c8d"
        ).pack(side="right")
        
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True)
        
  
        text_box = tk.Text(
            text_frame,
            wrap="none",  
            font=("Consolas", 11), 
            bg="#ffffff",
            fg="#2c3e50",
            selectbackground="#3498db",
            selectforeground="white",
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=15,
            spacing1=2, 
            spacing3=2
        )
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_box.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient="horizontal", command=text_box.xview)
        
        text_box.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        text_box.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        contenido_formateado = self.formatear_lista_espera(resultado)
        text_box.insert("1.0", contenido_formateado)
        text_box.configure(state="disabled")
        

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(15, 0))
        

        ttk.Button(
            button_frame,
            text="💾 Exportar",
            command=lambda: self.exportar_lista_espera(resultado)
        ).pack(side="left", padx=(0, 10))
        

        
        ttk.Button(
            button_frame,
            text="❌ Cerrar",
            command=resultado_ventana.destroy
        ).pack(side="right")
        
        resultado_ventana.bind('<Escape>', lambda e: resultado_ventana.destroy())
        
        resultado_ventana.focus_set()

    def formatear_lista_espera(self, contenido):
        """Mejora el formato visual del contenido"""
        lineas = contenido.split('\n')
        contenido_formateado = []
        
        for linea in lineas:
            if linea.strip():
                if linea.startswith('='):
                    contenido_formateado.append("=" * 60)
                elif linea.startswith('-'):
                    contenido_formateado.append("-" * 60)
                elif any(keyword in linea.lower() for keyword in ['paciente', 'id', 'nombre', 'edad']):
                    contenido_formateado.append(f"📋 {linea}")
                elif any(keyword in linea.lower() for keyword in ['urgente', 'crítico', 'prioridad']):
                    contenido_formateado.append(f"🚨 {linea}")
                else:
                    contenido_formateado.append(f"   {linea}")
            else:
                contenido_formateado.append("")
        
        return "\n".join(contenido_formateado)



    def exportar_lista_espera(self, contenido):
        """Exporta la lista a un archivo"""
        from tkinter import filedialog, messagebox
        from datetime import datetime
        
        filename = filedialog.asksaveasfilename(
            title="Exportar Lista de Espera",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile=f"lista_espera_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Lista de Espera - INCUCAI\n")
                    f.write(f"Generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(contenido)
                
                # Mostrar mensaje de confirmación
                messagebox.showinfo("Exportación exitosa", f"Lista exportada a:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")