import sys
from io import StringIO
import io
class OutputCapture:
    """Capturador de salida estándar"""
    
    def __init__(self):
        self.buffer = io.StringIO()
        self.original_stdout = sys.stdout
    
    def __enter__(self):
        sys.stdout = self.buffer
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout
    
    def get_output(self):
        return self.buffer.getvalue()