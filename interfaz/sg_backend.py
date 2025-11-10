"""
Wrapper para seleccionar el backend de PySimpleGUI.
Intenta importar PySimpleGUIQt (requiere PySide6 o PySide2). Si falla, cae a PySimpleGUI (Tkinter).
Exporta la variable `sg` que el resto de la UI puede usar como antes.
"""
import warnings

_sg = None
_backend = None
try:
    import PySimpleGUIQt as _sg  # intento Qt backend
    _backend = 'PySimpleGUIQt'
except Exception:
    try:
        import PySimpleGUI as _sg  # caigo a la versión Tkinter
        _backend = 'PySimpleGUI'
    except Exception:
        raise ImportError('No se encontró ni PySimpleGUIQt ni PySimpleGUI. Instale uno de ellos (recomiendo PySimpleGUIQt y PySide6).')

sg = _sg

def get_backend_name():
    return _backend

if _backend == 'PySimpleGUI':
    warnings.warn('Usando PySimpleGUI (Tkinter). Para mejor apariencia instale PySimpleGUIQt + PySide6.')
