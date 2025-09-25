from shiny import ui
from shinywidgets import output_widget
from .config import ALL_AREAS, SCATTER_SELECTOR, CSS_FILE

ui_page = ui.page_fluid(
    
   
    ui.include_css(CSS_FILE),

    ui.div({'class': 'info-panel'}, 
            ui.panel_title(title= ui.h1('Resultados del Examen de Admisión de la UNAM en el Sistema Escolarizado'), 
                   window_title="Visualizador de Resultados"),
            ui.hr(), 
            ui.p(ui.span({'class': 'text-about'}, '> Visualizador de datos desarrollado por Ricardo Martínez García')),
            
            # ui.HTML("<p style = 'color: #5e81ac'> > Visualizador de datos elaborado por Ricardo Martínez García</p>"), 
            ui.hr(), 
            ui.div(
                ui.p('El objetivo de esta página es mostrar de forma interactiva información relacionada sobre los resultados de Universidad Autónoma de México (UNAM).  Los datos fueron obtenidos de la páginas oficiales de la UNAM usando scraping, posteriormente fueron procesados para este análisis.'),
                ui.br(),
                ui.p('Este análisis está enfocado solamente en los resultados del examen de ingreso para el sistema escolarizado del año 2025, es decir, no se consideran las modalidades SUAyED y SUAyED Abierta.'),
                )
           ),
    
    # agregar una descripción que explique o indique el motivo de la creación de este visualizador de datos
    
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
                    title = ui.HTML("Total de<br>aspirantes"), 
                    value = ui.output_ui("total_aspirantes")
                    )
            ), 
            ui.column( 
                3, ui.value_box( 
                    title = ui.HTML("Aspirantes <br>seleccionados"), 
                    value = ui.output_ui("total_seleccionados"),
                    theme = ui.value_box_theme(bg = "#a3be8c")
                )
            ),
            ui.column(
                3,ui.value_box( 
                    title = ui.HTML("Aspirantes <br>rechazados"), 
                    value = ui.output_ui("total_rechazados"), 
                    theme = ui.value_box_theme(bg="#bf616a", fg="#eceff4")
                ) 
            ),
            ui.column(
                3,ui.value_box(
                    title = ui.HTML("Puntaje<br>perfecto"),
                    value = ui.output_ui('perfect_score'), 
                    theme=ui.value_box_theme(bg="#88c0d0")
                )
            )
        ),    
        ui.row(
            ui.column(
                12, 
                ui.card({'class': 'card-plot'},
                    ui.card_header(ui.h4('Distribución de aspirantes al sistema escolarizado'),
                    ),
                    output_widget("areas_chart"),
                    ui.card_footer(ui.p("Texto sobre el gráfico de pastel"))
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
                3,ui.input_select(
                    id = '_careers_demand_selector',
                    label = 'Seleccionar área',
                    choices= ALL_AREAS,
                    selected='all'
                )    
            ), ui.column(
                3, ui.input_select(
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
                    {'class': 'card-plot'},
                    ui.card_header(ui.output_ui("_careers_demand_title")),
                    output_widget(id = 'careers_demand'), 
                    ui.card_footer(ui.p("Texto para el gráfico de barras"))
                )
            )
        )        
    ),    
    
    ui.div({'class': 'square-information'},
        ui.div({'class': 'square-title'}, 
               ui.h3("¿Qué facultad o escuela tuvo mayor demanda?"),
        ),
        ui.row( 
            ui.column(
                3, ui.input_select(
                id = '_results_segment',
                label  = 'Segmentar por resultado', 
                choices = ['Si', 'No'], 
                selected = 'No'
                )
            )       
        ),
        ui.row( 
            ui.column(
                12,ui.card(
                    {'class': 'card-plot'},
                    ui.card_header(ui.output_ui(id = '_demanda_facultades_title')),
                    output_widget('demanda_facultades'),
                    ui.card_footer(ui.p("otro texto aquí"))
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
                3,
                ui.input_select( 
                    id = "_scatter_selector",
                    label = "Seleccionar área",
                    choices= ALL_AREAS,
                    selected= "all"                
                ) 
            ),
            ui.column(
                3, 
                ui.input_select(
                    id = "_scatter_x",
                    label = "Eje x",
                    choices= SCATTER_SELECTOR,
                    selected= 'oferta'
                )
            ),
            ui.column(
                3, 
                ui.input_select(
                    id = '_scatter_y', 
                    label = 'Eje y', 
                    choices= SCATTER_SELECTOR,
                    selected= 'demanda'
                )
            ), 
            ui.column(
                3, 
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
                    {'class': 'card-plot'},
                    ui.card_header( ui.output_ui(id = 'scatter_plot_title')),
                    output_widget("scatter_oda"), 
                    ui.card_footer(ui.p("Another generic text"))
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
                    {'class': 'card-plot'},
                    ui.card_header(ui.h4('Distribución de resultados')),
                    output_widget(id = 'results_distribution'),
                    ui.card_footer(ui.p("Bro, he really thinks he'll put something here"))
                )
            )
        )
    ),

    ui.hr(),
    
    ui.div({'class': 'info-panel'}, 
           ui.h3('Fuentes'),
           ui.HTML("""
            <p>Los datos fueron obtenidos de los siguientes sitios oficiales de la UNAM:</p>
            <ul>
                <li> Resultados área 1: <a href = 'https://www.dgae.unam.mx/Licenciatura2025/resultados/15.html'>https://www.dgae.unam.mx/Licenciatura2025/resultados/15.html</a></li>
                <li> Resultados área 2: <a href = 'https://www.dgae.unam.mx/Licenciatura2025/resultados/25.html'>https://www.dgae.unam.mx/Licenciatura2025/resultados/25.html</a></li>
                <li> Resultados área 3: <a href = 'https://www.dgae.unam.mx/Licenciatura2025/resultados/35.html'>https://www.dgae.unam.mx/Licenciatura2025/resultados/35.html</a></li>
                <li> Resultados área 4: <a href = 'https://www.dgae.unam.mx/Licenciatura2025/resultados/45.html'>https://www.dgae.unam.mx/Licenciatura2025/resultados/45.html</a></li>
                <li> Oferta 2025: <a href = 'https://www.dgae.unam.mx/Licenciatura2025/oferta_lugares/oferta_licenciatura2025.html'>https://www.dgae.unam.mx/Licenciatura2025/oferta_lugares/oferta_licenciatura2025.html</a> </li>
            </ul>
            <p><span style = 'font-style: italic; color: var(--nord10);'> > Nota: Es probable que las páginas no estén disponibles pronto</span></p>       
            """), 
           ui.hr(), 
           ui.HTML(""" 
            <footer>
                <p> Página desarrollada en Python con Shiny por Ricardo Martínez García</p>
                <p> El proceso de recolección de datos y desarrollo de esta página puedes consultarlo en mi repositorio de GitHub</p>
                <p> Cualquier duda o sugerencia es bienvenida, mis datos de contacto son los siguientes: [[REDACTED]]</p>

            </footer>       
                   
            """)
           
           
           )
    
    
    
    
)
