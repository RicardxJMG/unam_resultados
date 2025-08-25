#%%
from pathlib import Path
from typing import Generator, Optional
import sqlite3 as sql
import pandas as pd
from contextlib import contextmanager

import matplotlib.pyplot as plt     
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px

from shiny import App, Inputs,Outputs,Session, render, ui, reactive
# from shinywidgets import render_plotly, render_widget


#%%
DATA_PATH = Path(__file__).parent/"datos"/"processed"/"unam_resultados_2025.db"
QUERIES_PATH = Path(__file__).parent/"datos"/"queries"


@contextmanager
def database_connection(data_path: Path = DATA_PATH) -> Generator[sql.Connection, None, None]:
    conn: Optional[sql.Connection] = None
    try:
        conn = sql.connect(data_path)
        yield conn
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        raise
    finally:
        if conn is not None:
            conn.close()

def get_query(query: str) -> pd.DataFrame:
    with database_connection() as conn:
        return pd.read_sql(sql=query, con=conn)
    
queries_files: list[str] = [f'q{i+1}{ext}' for i,ext in enumerate(4*['.sql'])]
# q_text: list[str] = []
dfs: list[pd.DataFrame] = [] 

for q in queries_files: 
    q_text = (QUERIES_PATH/q).read_text(encoding = 'utf-8')
    dfs.append(get_query(query=q_text))

        
#%%     
# building app-web
# Observaciones para mejorar  
# 1. Definir el tamaño de los gráficos
# 2. Establecer cuales serán aquellos gráficos que reciban inputs
# 3. Establecer colores personalizados tanto para la página como para los gráficos
# 4. Establecer un estilo fijo para cada figura 
# 5. Por el momento cada grafico estará dentro de un div hasta encontrar una mejor opción.
# 6. Dejar para el final la configuración de html y css ,

_areas_dict = {'A1': 'Área 1', 'A2': 'Área 2', 'A3': 'Área 3', 'A4':'Área 4' }
_all_areas = {"all": 'Todos'}   
_all_areas.update(_areas_dict)
app_ui:App = ui.page_fluid(
    ui.panel_title("Análisis de Resultados de la UNAM 2025", "Análisis de resultados"),

    # ----  Gráfico de demanda por área
    ui.div(
        # Esta dividido en renglones para mostrar check boxes interactivos, tarjetas tipo KPI y un pie chart 
        ui.h3('Información general sobre el resultados del examen de admisión'),
        ui.row( 
            ui.input_checkbox_group(
                id="_areas_boxes", 
                label = "Seleccione área",
                choices= _areas_dict,
                selected = [] 
            ),   
        ),
        ui.row( 
            ui.column( 
                3,ui.value_box(
                    title = "Total de aspirantes", 
                    value = ui.output_ui("total_aspirantes") 
                    # theme`` = "primary"
                )
            ), 
            ui.column( 
                3, ui.value_box( 
                    title = "Aspirantes seleccionados", 
                    value = ui.output_ui("total_seleccionados")
                    # theme = "success"
                )
            ),
            ui.column(
                3,ui.value_box( 
                    title = "Aspirantes rechazados", 
                    value = ui.output_ui("total_rechazados")
                ) 
            ),
            ui.column(
                3,ui.value_box(
                    title ="Puntaje perfecto",
                    value = ui.output_ui('perfect_score'))
            )
        ),    
        ui.row(
            ui.column(
                12, 
                ui.card( 
                    ui.h4("Distribución de aspirantes"),
                    ui.output_plot("areas_chart")
                )
            )
        )
    ),
    
    ui.div(
        ui.h3('Carreras con mayor y menor demandas en 2025'),
        # este gráfico debe de tener un selector o checkbox para poder seleccionar entre las tres opciones de area 
        ui.row(
            ui.input_select(
                id = '_careers_demand_selector',
                label = 'Seleccionar áreas',
                choices= _all_areas,
                selected='all'
            )
        ),
        
        ui.row(
            ui.column(
                6, 
                ui.card(         
                    ui.output_plot('careers_higher_demand')  
                )
            ), 
            ui.column(
                6, 
                ui.card( 
                    ui.output_plot('careers_lower_demand')        
                )
            )  
        )        
    ), 
    ui.div(
        ui.h3('Top facultades con mayor demanda por área'), 
        ui.output_plot('demanda_facultades')
    ),
    # Gráficos sobre estado de acreditado de los aspirantes
    
    ui.div(
        ui.row()
        
        
        
        
    )
    
    
    
    
    
)


##### Definir servidor

def server(input: Inputs, output: Outputs, session: Session):
    
    # ---- 
    
    # Esta parte corresponde al primer panel sobre información general de demanda por área
    
    @reactive.calc
    def filtered_areas() -> pd.DataFrame: 
        df_areas = dfs[0].copy()
        selected_areas = input._areas_boxes()
        #print(selected_areas)
        if not selected_areas: 
            return df_areas 
        
        filtered_df = df_areas[df_areas['id_area'].isin(selected_areas)]
        
        return filtered_df
    
    @render.text 
    def total_aspirantes() -> str:
        df = filtered_areas()
        return f"{df['n_aspirantes'].sum(numeric_only=True):,}"
    
    @render.text
    def total_seleccionados() -> str: 
        df = filtered_areas() 
        return f"{df.query('resultado == "Seleccionado"').n_aspirantes.sum(numeric_only=True):,}"    
    
    @render.text
    def total_rechazados() -> str: 
        df = filtered_areas() 
        return f"{df.query('resultado == "No seleccionado"').n_aspirantes.sum(numeric_only=True):,}"    
    
    @render.text 
    def perfect_score() -> str:
        df = filtered_areas()
        return f'{df.query('puntaje_perfecto > 0').puntaje_perfecto.sum()}'
    
    @render.plot(alt='áreas chart') 
    def areas_chart():
        df_areas = filtered_areas()
        df_areas = df_areas.groupby(['id_area','area'], as_index=False)['n_aspirantes'].sum()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        ax.pie(x=df_areas['n_aspirantes'], 
               labels=df_areas['area'],
               autopct='%1.1f%%',
               startangle=90)
        
        # ax.set_title('Distribución de Aspirantes por Área')
        plt.tight_layout()
        return fig

        
    # -------
    
    # Esta parte corresponde a información sobre carreras más de mandadas por area
    
    @reactive.calc
    def careers_filter() -> pd.DataFrame: 
        df = dfs[2].copy()
        selected = input._careers_demand_selector()
        
        if selected == "all": return df
        
        return df.query(f"id_area == '{selected}' ")
    
    
    
    @render.plot(alt="carreras con mayor demanda")
    def careers_higher_demand(): 
        df_demanda = careers_filter()
        
        
        df_demanda = df_demanda.groupby(['id_area','carrera'], as_index=False)['n_aspirantes'].sum(numeric_only=True).sort_values(by = 'n_aspirantes').nlargest(n=7, columns='n_aspirantes')

        fig,ax = plt.subplots()
        ax.bar(data = df_demanda, x = 'carrera',height='n_aspirantes', width=0.8)

        return fig
    
    @render.plot(alt="carreras con menor demanda")
    def careers_lower_demand(): 
        df_demanda = careers_filter()
        df_demanda = df_demanda.groupby(['id_area','carrera'], as_index=False)['n_aspirantes'].sum(numeric_only=True).sort_values(by = 'n_aspirantes', ascending=True).nsmallest(n=7, columns='n_aspirantes')

        fig,ax = plt.subplots()
        ax.bar(data = df_demanda, x = 'carrera',height='n_aspirantes', width=0.8)

        return fig
    
    @output 
    @render.plot(alt = 'Escuelas con mayor demanda por área')
    def demanda_facultades(): 
        df_facultades = dfs[1]
        df_facultades = df_facultades.groupby(['id_area','facultad'])['n_aspirantes'].sum(numeric_only=True).reset_index().sort_values(by='n_aspirantes').nlargest(n =7, columns= 'n_aspirantes')

        fig, ax = plt.subplots()
        ax.bar(data = df_facultades, x = 'facultad', height='n_aspirantes', width=0.8)
    
        return fig
    
    
    
    
    
    
    
# Crear la aplicación
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
# %%
