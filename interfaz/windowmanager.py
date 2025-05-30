import tkinter as tk
class WindowManager:
    
    @staticmethod
    def center_window(window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def create_modal_window(parent, title, size):
        window = tk.Toplevel(parent)
        window.title(title)
        window.transient(parent)
        window.grab_set()
        window.resizable(True, True)
        
        width, height = map(int, size.split('x'))
        WindowManager.center_window(window, width, height)
        
        return window