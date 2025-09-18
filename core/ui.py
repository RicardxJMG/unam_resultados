from shiny import ui
from shinywidgets import output_widget
from .config import ALL_AREAS, SCATTER_SELECTOR, CSS_FILE


#import htmltools
# building app-web
# Observaciones para mejorar  
# 1. Definir el tamaño de los gráficos
# 2. Establecer un estilo fijo para cada figura 
# 3. Por el momento cada grafico estará dentro de un div hasta encontrar una mejor opción.
# 6. Dejar para el final la configuración de html y css ,


ui_page = ui.page_fluid(
    
   
    ui.include_css(CSS_FILE),
    
    ui.panel_title(title= 'Análisis de Resultados del Examen de Admisión de la UNAM en el Sistema Escolarizado', 
                   window_title="Análisis de Resultados"),
    ui.div({'class': 'square-information'},
        ui.p('El objetivo de esta página es reflejar la distante brecha que existe entre los jóvenes que aspiran a ingresar en algunas de las carreras impartidas en la Universidad Nacional Autónoma de México (UNAM), cuantos de ellos son seleccionados y cuantos de ellos son rechazados.'),
        ui.br(),
        ui.p('Este análisis está enfocado solamente en los resultados del examen de ingreso para el sistema escolarizado del año 2025, es decir, no se consideran las modalidades SUAyED y SUAyED Abierta.'),
    ),
    
    
    # ----  Gráfico de demanda por área
    ui.div({'class': 'square-information'},
        # Esta dividido en renglones para mostrar check boxes interactivos, tarjetas tipo KPI y un pie chart 

        ui.div({'class': 'square-title'}, ui.h3('Información general sobre los resultados del examen de admisión'),
        ),
         ui.row( 
            ui.input_select(
                id="_pie_selector", 
                label = "Seleccione área",
                choices= ALL_AREAS,
                selected = [] 
            ),   
        ),
        ui.row( 
            ui.column( 
                3, ui.value_box(
                    title = "Total de aspirantes", 
                    value = ui.output_ui("total_aspirantes")
                    )
            ), 
            ui.column( 
                3, ui.value_box( 
                    title = "Aspirantes seleccionados", 
                    value = ui.output_ui("total_seleccionados")
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
                    ui.h4('Distribución de aspirantes al sistema escolarizado'),
                    output_widget("areas_chart")
                )
            )
        )
    ),
    
    # este gráfico debe de tener un selector o checkbox para poder seleccionar entre las tres opciones de area 
    ui.div({'class': 'square-information'},
        ui.div({'class': 'square-title'},
               ui.h3('¿Cuáles fueron las carreras con mayor y menor demanda?'),
        ),
        ui.row(
            ui.column(  
                4,ui.input_select(
                    id = '_careers_demand_selector',
                    label = 'Seleccionar área',
                    choices= ALL_AREAS,
                    selected='all'
                )    
            ), ui.column(
                4, ui.input_select(
                    id = '_higher_lower',
                    label = 'Tipo de demanda',
                    choices = ['Mayor','Menor'], 
                    selected= 'Mayor'    

                )

            )
        ),
        
        ui.row(
            ui.column(
                12, 
                ui.card(       
                    ui.output_ui("_careers_demand_title"), 
                    output_widget(id = 'careers_demand')  
                )
            )
        )        
    ),    
    
    ui.div({'class': 'square-information'},
        ui.div({'class': 'square-title'}, 
               ui.h3("¿Qué facultad o escuela tuvo mayor demanda?"),
        ),
        ui.row( 
            ui.input_select(
                id = '_results_segment',
                label  = 'Segmentar por resultado', 
                choices = ['Si', 'No'], 
                selected = 'No'
            )       
        ),
        ui.row( 
            ui.column(
                12,ui.card(
                    ui.output_ui(id = '_demanda_facultades_title'),
                    output_widget('demanda_facultades')           
                ) 
            )          
        )
    ),
    
    # Gráfico scatter
    
    ui.div({'class': 'square-information'},
        ui.div({'class': 'square-title'}, 
               ui.h3("¿Qué relación existe entre aciertos mínimos, demanda y total de seleccionados?"),
        ),
        ui.row(
            ui.column(
                2,
                ui.input_select( 
                    id = "_scatter_selector",
                    label = "Seleccionar área",
                    choices= ALL_AREAS,
                    selected= "all"                
                ) 
            ),
            ui.column(
                2, 
                ui.input_select(
                    id = "_scatter_x",
                    label = "Eje x",
                    choices= SCATTER_SELECTOR,
                    selected= 'oferta'
                )
            ),
            ui.column(
                2, 
                ui.input_select(
                    id = '_scatter_y', 
                    label = 'Eje y', 
                    choices= SCATTER_SELECTOR,
                    selected= 'demanda'
                )
            ), 
            ui.column(
                2, 
                ui.input_select( 
                    id = '_scatter_size',
                    label = 'Tamaño',
                    choices = SCATTER_SELECTOR, 
                    selected= 'aciertos_minimos'
                )
            )   
        ),
        ui.row(
            ui.column(
                12, ui.card( 
                    ui.output_ui(id = 'scatter_plot_title'),
                    output_widget("scatter_oda")                
                )
            )
        )    
    ), 
    
    ui.div({'class': 'square-information'},
        ui.div({'class': 'square-title'}, 
                ui.h3("¿Cómo fue la distribución del puntaje obtenido por los aspirantes?")
       ),
        ui.row(
            ui.column(
                2, 
                ui.input_select(
                    id = '_dist_areas', 
                    label = "Seleccionar área", 
                    choices= ALL_AREAS, 
                    selected= 'all'
                )
            )
        ), 
        ui.row(
            ui.column(
                12,ui.card(
                    ui.h4('Distribución de resultados'),
                    output_widget(id = 'results_distribution')
                )
            )
        )
    )
)
