from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .contentformater import ContentFormatter
class FileExporter:
    """Gestor de exportación de archivos"""
    
    @staticmethod
    def export_wait_list(parent_window, content):
        """Exporta la lista de espera a un archivo de texto"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_filename = f"lista_espera_{timestamp}.txt"
        
        filename = filedialog.asksaveasfilename(
            parent=parent_window,
            title="💾 Exportar Lista de Espera",
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ],
            initialfile=default_filename
        )
        
        if not filename:
            return False
        
        try:
            FileExporter._write_export_file(filename, content)
            FileExporter._show_export_success(filename)
            return True
        except Exception as e:
            FileExporter._show_export_error(str(e))
            return False
    
    @staticmethod
    def _write_export_file(filename, content):
        """Escribe el archivo de exportación"""
        current_time = datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("=" * 70 + "\n")
            file.write("    LISTA DE ESPERA - SISTEMA INCUCAI\n")
            file.write("=" * 70 + "\n\n")
            file.write(f"📅 Generado el: {current_time}\n")
            file.write(f"👥 Total de pacientes: {ContentFormatter.count_patients(content)}\n")
            file.write("\n" + "=" * 70 + "\n\n")
            file.write(content)
            file.write("\n\n" + "=" * 70 + "\n")
            file.write("Fin del reporte - Sistema INCUCAI\n")
    
    @staticmethod
    def _show_export_success(filename):
        """Muestra mensaje de éxito en la exportación"""
        messagebox.showinfo(
            "✅ Exportación Exitosa",
            f"Lista de espera exportada correctamente:\n\n📁 {filename}",
            icon='info'
        )
    
    @staticmethod
    def _show_export_error(error_message):
        """Muestra mensaje de error en la exportación"""
        messagebox.showerror(
            "❌ Error de Exportación",
            f"No se pudo exportar la lista:\n\n{error_message}",
            icon='error'
        )