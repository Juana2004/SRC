from .uiconstants import UIConstants
from tkinter import ttk
class StyleManager:
    """Gestor de estilos de la aplicación"""
    
    def __init__(self):
        self.style = ttk.Style()
        self._setup_theme()
    
    def _setup_theme(self):
        """Configura el tema visual de la aplicación"""
        self.style.theme_use("clam")
        self._configure_base_styles()
        self._configure_custom_styles()
    
    def _configure_base_styles(self):
        """Configura estilos base de widgets"""
        self.style.configure("TLabel", 
                           font=UIConstants.FONTS['default'], 
                           background=UIConstants.COLORS['light'])
        
        self.style.configure("TButton", 
                           font=UIConstants.FONTS['default'], 
                           padding=8)
        
        self.style.configure("TEntry", 
                           font=UIConstants.FONTS['default'])
        
        self.style.configure("TFrame", 
                           background=UIConstants.COLORS['light'])
    
    def _configure_custom_styles(self):
        """Configura estilos personalizados"""
        # Header principal
        self.style.configure("Header.TLabel",
                           font=UIConstants.FONTS['header'],
                           background=UIConstants.COLORS['light'],
                           foreground=UIConstants.COLORS['primary'])
        
        # Subheader
        self.style.configure("Subheader.TLabel",
                           font=UIConstants.FONTS['subheader'],
                           foreground=UIConstants.COLORS['primary'])
        
        # Botón principal
        self.style.configure("Primary.TButton",
                           foreground="white",
                           background=UIConstants.COLORS['secondary'])
        
        self.style.map("Primary.TButton",
                      background=[("active", UIConstants.COLORS['primary']),
                                ("pressed", UIConstants.COLORS['dark'])])
        
        # Frame tipo tarjeta
        self.style.configure("Card.TFrame",
                           background=UIConstants.COLORS['background'],
                           relief="solid",
                           borderwidth=1)
        
        # Labels informativos
        self.style.configure("Info.TLabel",
                           font=UIConstants.FONTS['small'],
                           foreground=UIConstants.COLORS['text_secondary'])
