"""
Core package para la aplicación web de análisis de resultados UNAM.

Este paquete contiene los componentes principales de la aplicación:
- server.py: Lógica del servidor Shiny y funciones reactivas
- ui.py: Interfaz de la página y componentes visuales

El paquete está estructurado para facilitar el mantenimiento y la
organización del código de la aplicación web de visualización de
resultados del examen de admisión de la UNAM para futuros resultados.
"""

from .ui import ui_page
from .server import server

__all__ = [
    'ui_page',
    'server'
]