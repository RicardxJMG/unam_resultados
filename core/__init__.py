"""
Core package para la aplicación web de análisis de resultados UNAM.

Este paquete contiene los componentes principales de la aplicación:
- config.py: Configuración global, constantes y gestión de colores
- data_manager.py: Gestión de conexiones a base de datos SQLite
- server.py: Lógica del servidor Shiny y funciones reactivas
- ui.py: Interfaz de usuario y componentes visuales

El paquete está estructurado para facilitar el mantenimiento y la
organización del código de la aplicación web de visualización de
resultados del examen de admisión de la UNAM.
"""

# Importaciones principales
from .config import (
    AREA_COLORS, AREA_COLORS_ALT, RESULTS, RESULTS_COLORS,
    ALL_AREAS, AREAS_DICT, SCATTER_SELECTOR,
    DataManager, dfs
)
from .ui import ui_page
from .server import server
from .data_manager import DataManager

# Define los elementos que estarán disponibles al usar 'from core import *'
__all__ = [
    # Componentes principales
    'ui_page',
    'server',
    'DataManager',
    
    # Constantes y configuraciones
    'AREA_COLORS',
    'AREA_COLORS_ALT',
    'RESULTS',
    'RESULTS_COLORS',
    'ALL_AREAS',
    'AREAS_DICT',
    'SCATTER_SELECTOR',
    'dfs'
]