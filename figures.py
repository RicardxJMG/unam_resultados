#%%
import matplotlib.pyplot as plt 
import seaborn as sns 
# import plotly
import pandas as pd 
from pathlib import Path
import sqlite3 as sql 
import numpy as np

from matplotlib import rcParams
import matplotlib.pyplot as plt     
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px

from shiny import App, Inputs, Outputs, Session, render, ui

palette = sns.color_palette("Dark2", as_cmap=False)
colors = [f'rgb({int(r*255)}, {int(g*255)}, {int(b*255)})' for r, g, b in palette]


#%%
DATA_PATH = Path(__file__).parent/"datos"/"processed"/"unam_resultados_2025.db"
QUERIES_PATH = Path(__file__).parent/"datos"/"queries"

rcParams.update({
    'figure.figsize': (10, 6),
    'figure.facecolor': '#f9f1d2',
    'axes.facecolor': '#f5ecc9',
    'axes.titlesize': 16,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.spines.top': False,
    'axes.spines.right': False
})

# Similar configuration as matplotlib
custom_template = go.layout.Template(
    layout=go.Layout(
        plot_bgcolor='#f9f1d2',  # Similar to figure.facecolor
        paper_bgcolor='#f5ecc9',  # Similar to axes.facecolor
        title_font = dict(size=28, color="black", weight="bold"),
        font_size=12,
        colorway = colors,
        colorscale=dict(sequential=colors),
        xaxis=dict(
            title_font_size=14,
            tickfont_size=10,
            showline=False,
            mirror=False,
        ),
        yaxis=dict(
            title_font_size=14,
            tickfont_size=10,
            showline=False,
            mirror=False,
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
        yaxis_showspikes=False,

    )
)

# Aplicar el template como predeterminado
pio.templates["custom"] = custom_template




def connect_database(data_path: str = DATA_PATH) -> sql.Connection|None: 
    con = None
    try: 
        con = sql.connect(DATA_PATH)
    except:
        print("Error al conectarse a la base de datos")
    finally:
        return con

#%%
if __name__ == '__main__':
    
    aval_queries = [f'q{i+1}{ext}' for i,ext in enumerate(4*['.sql'])]
    
    conn = connect_database()


    
    df = pd.read_sql(query, con = conn)
    df = df.groupby('area')['n_aspirantes'].sum().reset_index()
    
    #%%
    fig, axes = plt.subplots()
    axes.pie(x=df.n_aspirantes,labels=df.area)
    
    conn.close()
    
    
    


