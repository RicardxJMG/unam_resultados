from shiny import ui
from shinywidgets import output_widget, render_widget
from config import _all_areas, _scatter_selector


# building app-web
# Observaciones para mejorar  
# 1. Definir el tamaño de los gráficos
# 2. Establecer un estilo fijo para cada figura 
# 3. Por el momento cada grafico estará dentro de un div hasta encontrar una mejor opción.
# 6. Dejar para el final la configuración de html y css ,


ui_page = ui.page_fluid(
    ui.panel_title("Análisis de Resultados de la UNAM 2025 en el Sistema Escolarizado", "Análisis de Resultados"),
    ui.p('El objetivo de esta página es reflejar la distante brecha que existe entre los jóvenes que aspiran a ingresar en algunas de las carreras impartidas en la Universidad Nacional Autónoma de México (UNAM), cuantos de ellos son seleccionados y cuantos de ellos son rechazados.'),
    ui.br(),
    ui.p('Este análisis está enfocado solamente en los resultados del examen de ingreso para el sistema escolarizado del año 2025, es decir, no se consideran las modalidades SUAyED y SUAyED Abierta.'),
    # ----  Gráfico de demanda por área
    ui.div(
        # Esta dividido en renglones para mostrar check boxes interactivos, tarjetas tipo KPI y un pie chart 

        ui.h3('Información general sobre los resultados del examen de admisión'),
        ui.row( 
            ui.input_select(
                id="_pie_selector", 
                label = "Seleccione área",
                choices= _all_areas,
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
                    ui.h4(ui.HTML('<b>Distribución de aspirantes al sistema escolarizado</b>')),
                    output_widget("areas_chart")
                )
            )
        )
    ),
    
    ui.div(
        ui.h3('Las carreras con mayor y menor demanda en 2025'),
        # este gráfico debe de tener un selector o checkbox para poder seleccionar entre las tres opciones de area 
        ui.row(
            ui.column(  
                4,ui.input_select(
                    id = '_careers_demand_selector',
                    label = 'Seleccionar área',
                    choices= _all_areas,
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
            # ui.column(
            #     4,ui.input_select(
            #         id = '_results_demand_selector',
            #         label = 'Mostrar resultados',
            #         choices= ["Si", "No"],
            #         selected='No'
            #     )
            # )
            
            
        ),
        
        ui.row(
            ui.column(
                12, 
                ui.card(       
                    ui.h4(ui.HTML('<b>Este titulo debe ser dinámico</b>')),  
                    output_widget('careers_demand')  
                )
            )
        )        
    ),    
    ui.div(
        ui.h3("Demanda por  facultad y/o escuela"),
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
                    ui.h4('Facultades de mayor a menor demanda (sin-con segmentar por resultado)'),
                    output_widget('demanda_facultades')           
                ) 
            )          
        )
    ),
    
    # Gráfico scatter
    
    ui.div(
        ui.h3("¿Qué relación existe entre aciertos mínimos, demanda y total de seleccionados?"),
        ui.row(
            ui.column(
                2,
                ui.input_select( 
                    id = "_scatter_selector",
                    label = "Seleccionar área",
                    choices= _all_areas,
                    selected= "all"                
                ) 
            ),
            ui.column(
                2, 
                ui.input_select(
                    id = "_scatter_x",
                    label = "Eje x",
                    choices= _scatter_selector,
                    selected= 'oferta'
                )
            ),
            ui.column(
                2, 
                ui.input_select(
                    id = '_scatter_y', 
                    label = 'Eje y', 
                    choices= _scatter_selector,
                    selected= 'demanda'
                )
            ), 
            ui.column(
                2, 
                ui.input_select( 
                    id = '_scatter_size',
                    label = 'Tamaño',
                    choices = _scatter_selector, 
                    selected= 'aciertos_minimos'
                )
            )   
        ),
        ui.row(
            ui.column(
                12, ui.card( 
                    ui.h4("Relación entre EJE X, EJE Y y PESO"),
                    output_widget("scatter_oda")                
                )
            )
        )    
    ), 
    
    ui.div(
        ui.h3("Distribución de los resultados obtenidos por los aspirantes"),
        ui.row(
            ui.column(
                2, 
                ui.input_select(
                    id = '_dist_areas', 
                    label = "Seleccionar área", 
                    choices= _all_areas, 
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
