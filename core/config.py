from .data_manager import DataManager
from pathlib import Path
import plotly.io as pio
import plotly.graph_objects as go

# Ajustando rutas para trabajar desde la carpeta core
DATA_PATH = Path(__file__).parent.parent/"datos"/"processed"/"unam_resultados_2025.db"
QUERIES_PATH = Path(__file__).parent.parent/"datos"/"queries"

# Inicializar el gestor de datos y cargar las consultas
db = DataManager(DATA_PATH)
dfs = db.load_queries(QUERIES_PATH)


AREA_COLORS = {
    "A1": "#1B3B6F",  # Azul marino
    "A2": "#2E8B57",  # Verde bosque
    "A3": "#DAA520",  # Dorado / Ámbar
    "A4": "#800020"   # Burdeos / Vino
}

AREA_COLORS_ALT = {
    "A1": "#0072B2",  # Azul brillante
    "A2": "#009E73",  # Verde turquesa
    "A3": "#E69F00",  # Naranja dorado
    "A4": "#CC79A7"   # Magenta suave
}

RESULTS = ['Seleccionado', 'No seleccionado', 'No presentado', 'Cancelado']

RESULTS_COLORS = {
    RESULTS[0]: "#2CA02C",   # Verde brillante → éxito / aprobado
    RESULTS[1]: "#D62728", # Rojo intenso → rechazo
    RESULTS[2]: "#FF7F0E",   # Naranja → ausencia, advertencia
    RESULTS[3]: "#7F7F7F"        # Gris neutro → estado inactivo
}


#  Templeate para ploty, se crea el templeate 'custom' y se combina con alguno de los ya existentes


GO_TEMPLETE  = go.layout.Template(
        layout=go.Layout(
        plot_bgcolor="#f0ebd5",  # Similar to figure.facecolor
        paper_bgcolor="#e9e0bb",  # Similar to axes.facecolor
        title_font = dict(size=28, color="black", weight="bold"),
        font_size=12,
        xaxis=dict(
            title_font_size=14,
            tickfont_size=11,
            showline=False,
            mirror=False        
        ),
        yaxis=dict(
            title_font_size=14,
            tickfont_size=11,
            showline=False,
            mirror=False
       
        ),
        legend=dict(
            title_font=dict(size=14, weight="bold"),
            font=dict(size=12)
        ),
        annotations=[dict(
            font=dict(size=20, weight="bold")
        )],
        # Deshabilitar spines (bordes) superior y derecho
        xaxis_showspikes=False,
        yaxis_showspikes=False
    )
)

pio.templates['custom'] = GO_TEMPLETE
pio.templates.default = 'plotly_white+custom'


AREAS_DICT = {'A1': 'Área 1', 'A2': 'Área 2', 'A3': 'Área 3', 'A4':'Área 4' }
ALL_AREAS = {"all": 'Todos'}   
ALL_AREAS.update(AREAS_DICT)
SCATTER_SELECTOR = {'demanda': 'Demanda', 'oferta': 'Oferta', 'aciertos_minimos': 'Aciertos mínimos', 'seleccionados': 'Seleccionados'}

CSS_FILE = Path(__file__).parent / 'styles' / 'style.css'