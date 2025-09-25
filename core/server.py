import pandas as pd
from numpy import interp
from plotly.subplots import make_subplots
from shiny import Inputs,Outputs,Session, render, reactive, ui
from shinywidgets import render_widget

from .config import *



def server(input: Inputs, output: Outputs, session: Session):
    
    # ---- 
    
    # Esta parte corresponde al primer panel sobre información general de demanda por área
    
    @reactive.calc
    def pull_area() -> tuple[int,pd.DataFrame]: 
        df = dfs[0].copy()
        selected_area = input._pie_selector()
        
        if selected_area == 'all': 
            return (-1, df)

        return (int(selected_area[1])-1, df.query(f'id_area =="{selected_area}"'))
    
    
    @render.text 
    def total_aspirantes() -> str:
        _,df = pull_area()
        return f"{df['n_aspirantes'].sum(numeric_only=True):,}"
    
    @render.text
    def total_seleccionados() -> str: 
        _,df = pull_area()
        return f"{df.query('resultado == "Seleccionado"').n_aspirantes.sum(numeric_only=True):,}"    
    
    @render.text
    def total_rechazados() -> str: 
        _,df = pull_area()
        return f"{df.query('resultado == "No seleccionado"').n_aspirantes.sum(numeric_only=True):,}"    
    
    @render.text 
    def perfect_score() -> str:
        _,df = pull_area()
        return f'{df.query('puntaje_perfecto > 0').puntaje_perfecto.sum()}'
    
    @render_widget() 
    def areas_chart():
        df_areas = dfs[0].copy()
        df_areas = df_areas.groupby(['id_area','area'], as_index=False)['n_aspirantes'].sum()
        
        pull_slice,_ = pull_area()
        pull = 4*[0]
        
        pull[pull_slice] = pull[pull_slice] + 0.2 if pull_slice>=0 else 0
        
        
        labels = df_areas.area.unique().tolist()
        
        
        # ¿será mejor realizar cuatro pie charts?
        fig = make_subplots(rows = 1, cols =1, specs= [[{'type':'domain'}]])
        
        fig.add_trace(
            trace = go.Pie( 
                labels = labels, 
                values = df_areas.n_aspirantes,
                textinfo='percent+value', textposition='inside', 
                marker = dict(colors = [AREA_COLORS[a] for a in df_areas.id_area]),
                pull=pull),
            col=1, row=1)
        fig.update_traces(hole = .3, hoverinfo = 'label+value')
        fig.update_layout(legend = dict(title = "Área"))
    
        
        
        
        return fig

        
    # -------
    
    # Esta parte corresponde a información sobre carreras más de mandadas por area
    
    @reactive.calc
    def careers_area_filter() -> pd.DataFrame: 
        df = dfs[2].copy()
        selected = input._careers_demand_selector()
        
        if selected == "all": return df
        
        return df.query(f"id_area == '{selected}' ")
    
    
    @render.ui 
    def _careers_demand_title(): 
        demand_type = "mayor" if input._higher_lower() == "Mayor" else "menor"
        return ui.h4(f"Top 10 carreras con {demand_type} demanda")
   
    @reactive.calc 
    def filter_demand() -> pd.DataFrame:
        df = careers_area_filter()
        df = df.groupby(by = ['id_area', 'carrera'])['n_aspirantes'].sum(numeric_only=True).reset_index()
        
        selected = input._higher_lower() 
        
        if selected == 'Menor':
            return df.nsmallest(n = 10, columns= ['n_aspirantes']).sort_values( by = 'n_aspirantes')
        
        return df.nlargest(n = 10, columns= ['n_aspirantes'])#.sort_values(by = 'n_aspirantes', ascending = False)

    @render_widget
    def careers_demand(): 
        df = filter_demand() 
        fig = make_subplots(cols =1, rows=1,  specs=[[{'type': 'xy'}]])
        
        fig.add_trace(
            trace= go.Bar(
                x = df.carrera.str.capitalize(), 
                y = df.n_aspirantes, 
                marker=dict(color=[AREA_COLORS[a] for a in df.id_area]),
                showlegend=False,
                width = 0.6
            ), 
            col=1,row=1
        )
        
        for area in ['A1','A2','A3','A4']:
            fig.add_trace(
                go.Bar(
                    x=[None], y=[None],
                    marker=dict(color=AREA_COLORS[area]),
                    name=AREAS_DICT[area],  
                    showlegend=True
                )
            )
            
        fig.update_layout(legend = dict(title = 'Áreas'))
        
        
        
        
        return fig
    
     # -------
    
    # Esta parte corresponde a información sobre la demanda de facultades, y  una opción de mostrar el tipo de acreditado
   
    
    @reactive.calc
    def facultad_segmentar() -> pd.DataFrame:
        df = dfs[1].copy()
        selected = input._results_segment() 
        
        return df if selected == 'Si' else \
            df.groupby(by = 'facultad')['n_aspirantes'].sum(numeric_only = True).reset_index()
    
    
    @render.ui 
    def _demanda_facultades_title(): 
        selected = input._results_segment()
        title = 'Facultades con mayor a menor demanda'
        if selected == 'Si':
            return ui.h4(title + " segmentado por resultado")

        return ui.h4(title)
    
    @render_widget()
    def demanda_facultades():
        df_facultades = facultad_segmentar()

        # Orden de facultades según el total de aspirantes (para que se mantenga)
        orden_facultades = (df_facultades.groupby("facultad")["n_aspirantes"].sum().sort_values().index.tolist())

        fig = make_subplots(rows=1, cols=1)

        if "id_area" not in df_facultades.columns:
            fig.add_trace(
                go.Bar(
                    x=df_facultades["n_aspirantes"],
                    y=df_facultades["facultad"],
                    orientation="h",
                    marker=dict(color="#5e81ac"),
                    name="Total",
                    showlegend=False,
                    width = 0.5
                )
            )
        else:
            for resultado in df_facultades["resultado"].unique():
                tmp = df_facultades[df_facultades["resultado"] == resultado]

                fig.add_trace(
                    go.Bar(
                        x=tmp["n_aspirantes"],
                        y=tmp["facultad"],
                        orientation="h",
                        marker=dict( color = [RESULTS_COLORS[r] for r in tmp.resultado] ),
                        name=resultado,
                        width = 0.5
                    )
                )

            fig.update_layout(legend = dict(title = 'Resultado', y  = -.08),barmode="stack")
       
        fig.update_layout(height = 675)
        fig.update_yaxes(categoryorder="array", categoryarray=orden_facultades)

        return fig
    
     # -------
    
    # Esta parte corresponde al scatter plot.
    
    @reactive.calc
    def scatter_data() -> list[pd.DataFrame, str]:
        df = dfs[4].copy()
        area_selected = input._scatter_selector()
        x_axis = input._scatter_x()
        y_axis = input._scatter_y()
        size = input._scatter_size()
        
        return [df,area_selected, x_axis, y_axis, size]
    
    
    @render.ui 
    def scatter_plot_title(): 
        x_axis = SCATTER_SELECTOR[input._scatter_x()]
        y_axis = SCATTER_SELECTOR[input._scatter_y()]
        s = SCATTER_SELECTOR[input._scatter_size()] 
        
        
        return ui.h4(f'Relación entre {x_axis}, {y_axis} ponderado por {s}')    
    
    
    @render_widget
    def scatter_oda():
        df, area, x_axis, y_axis, size = scatter_data()  # Use the calc function
        
        if area != 'all': df = df.query(f'id_area == "{area}"')
        
        # testear según se vea bonito
        
        min_marker = 8
        max_marker = 50
        scaled_size = interp(x = df[size], xp = (df[size].min(), df[size].max()), fp = (min_marker, max_marker))
        
        fig = make_subplots(rows = 2, cols =2, 
                            column_widths= [0.8, 0.2], row_heights=[0.2,0.8],
                            horizontal_spacing= 0.02, vertical_spacing= 0.02,
                            specs = [[{'type': 'histogram'}, {'type': 'histogram'}], [{'type': 'scatter'}, {'type': 'histogram'}]], 
                            x_title=x_axis, 
                            y_title=y_axis)
        
        fig.add_trace( 
            trace = go.Scatter(x = df[x_axis], y = df[y_axis], mode='markers',
                         marker= dict(size = scaled_size, color = [AREA_COLORS[a] for a in df.id_area]), 
                         text= df[size]),
            row = 2, col=1
        )
        
        fig.add_trace(
            trace = go.Histogram(
                  x = df[x_axis], nbinsx= 75),
            row = 1, col=1
        )
        
        fig.add_trace(
            trace = go.Histogram( 
                y = df[y_axis], nbinsy=75),
            row = 2, col=2
        )
        
        fig.update_layout(showlegend = False, bargap = 0.05, margin=dict(t=20, r=20, b=20, l=20))
        fig.update_xaxes(showticklabels = False, row = 1, col = 1)
        fig.update_yaxes(showticklabels = False, row = 2, col = 2)
    

        
        # ax.scatter(data=df_scatter, x=x_axis, y=y_axis, s=size)
        
        return fig
    
    
    # -------------------
    
    # Esta parte corresponde al gráfico de distribución de resultados
    
    
    @reactive.calc 
    def distribution_filter() -> pd.DataFrame: 
        area   = input._dist_areas()
        sql = "SELECT * FROM resultados_2025"
        return db.get_query(query=sql)        
                
        
        
    @render_widget
    def results_distribution() : 
        df = distribution_filter() # ajustar este filtro porquue no faz nada kkkkkkk
        
        fig = go.Figure()
        
        for area, area_df in df.groupby(['id_area']): 
            x = len(area_df)*[AREAS_DICT[area[0]]]
            fig.add_trace(
                go.Violin(
                          x = x,
                          y = area_df.puntaje.dropna(),
                          line_color  = AREA_COLORS[area[0]], 
                          name = AREAS_DICT[area[0]],
                          fillcolor= AREA_COLORS[area[0]], 
                          opacity= 0.75,   
                          meanline_visible = True,  
                          meanline_color = "#D5D820",
                          width=0.5)
                )
        
        return fig
    
   
