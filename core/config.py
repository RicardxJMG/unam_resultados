from .data_manager import DataManager
from pathlib import Path
import plotly.io as pio
import plotly.graph_objects as go

# Ajustando rutas para trabajar desde la carpeta core
DATA_PATH = Path(__file__).parent.parent/"datos"/"processed"/"unam_resultados_2025.db"
QUERIES_PATH = Path(__file__).parent.parent/"datos"/"queries"

# Inicializar el gestor de datos y cargar las consultas
db = DataManager(DATA_PATH)
dfs = db.load_queries(queries_path=QUERIES_PATH,n = 6)


AREA_COLORS = {
    "A1": "#5E81AC",  # nord 10
    "A2": "#A3BE8C",  # nord 14
    "A3": "#EBCB8B",  # nord 13
    "A4": "#B48EAD",   # nord 15
    "Área 1": "#5E81AC",  # nord 10
    "Área 2": "#A3BE8C",  # nord 14
    "Área 3": "#EBCB8B",  # nord 13
    "Área 4": "#B48EAD",   # nord 15
}

AREA_COLORS_ALT = {
    "A1": "#0072B2",  # Azul brillante
    "A2": "#009E73",  # Verde turquesa
    "A3": "#E69F00",  # Naranja dorado
    "A4": "#CC79A7"   # Magenta suave
}

RESULTS = ['Seleccionado', 'No seleccionado', 'No presentado', 'Cancelado']

RESULTS_COLORS = {
    RESULTS[0]: "#A3BE8C",   # Verde brillante → éxito / aprobado
    RESULTS[1]: "#BF616A", # Rojo intenso → rechazo
    RESULTS[2]: "#D08770",   # Naranja → ausencia, advertencia
    RESULTS[3]: "#4C566A"       # Gris neutro → estado inactivo
}


#  Templeate para ploty, se crea el templeate 'custom' y se combina con alguno de los ya existentes


GO_TEMPLETE  = go.layout.Template(
        layout=go.Layout(
        plot_bgcolor="#e5e9f0",  # nord5
        paper_bgcolor="#d8dee9",  # nord4
        
        font = dict( 
            family = "Quicksand",  
            color = "#2e3440"
        ),
        
        xaxis = dict(
            title_font_size=14,
            tickfont_size=11,
            showline=False,
            mirror=False,    
            color = "#3b4252"  
        ),
        yaxis=dict(
            title_font_size=14,
            tickfont_size=11,
            showline=False,
            mirror=False,
            color = "#3b4252"
        ),
        legend=dict(
            title_font=dict(size=14, weight="bold"),
            font=dict(size=12), 
            orientation = 'h', 
            yanchor="top",
            y=1.18,
            xanchor="center",
            x=0.5
        ),
        annotations=[dict(
            font=dict(size=20, weight="bold")
        )],
        xaxis_showspikes=False,
        yaxis_showspikes=False, 
        height= 300,
       #  margin=dict(t=100, b=100, l=100, r=100),  # espacio para título y leyenda
    )
)

pio.templates['custom'] = GO_TEMPLETE
pio.templates.default = 'plotly_white+custom'


AREAS_DICT = {'A1': 'Área 1', 'A2': 'Área 2', 'A3': 'Área 3', 'A4':'Área 4' }
ALL_AREAS = {"all": 'Todos'}   
ALL_AREAS.update(AREAS_DICT)
SCATTER_SELECTOR = {'demanda': 'Demanda', 'oferta': 'Oferta', 'aciertos_minimos': 'Aciertos mínimos', 'seleccionados': 'Seleccionados'}

CSS_FILE = Path(__file__).parent / 'styles' / 'style.css'

CAREERS_LIST = dfs[5].carrera.unique().tolist()