# Scraping de oferta y resultados de la UNAM 2025

Este repositorio contiene scripts desarrollados en Python para automatizar la extracción de información sobre los resultados del examen de admisión de la UNAM a nivel licenciatura en el sistema escolarizado, correspondiente al año 2025.

## Descripción general

Este repositorio incluye dos scripts principales:

1. **scraping_puntaje**: Accede a cada una de las páginas de resultados por área, carrera y escuela asociadas para obtener tres tablas distintas: una con el contenido general de los resultados, otra con los nombres de las facultades/escuelas, y otra relacionada con las carreras. Los datos pueden consultarse en: [Resultados área 1](https://www.dgae.unam.mx/Licenciatura2025/resultados/15.html), [Resultados área 2](https://www.dgae.unam.mx/Licenciatura2025/resultados/25.html), [Resultados área 3](https://www.dgae.unam.mx/Licenciatura2025/resultados/35.html) y [Resultados área 4](https://www.dgae.unam.mx/Licenciatura2025/resultados/45.html).

2. **scraping_oferta**: Extrae la tabla de oferta de lugares de los años 2024 y 2025 para cada carrera y área. La tabla fue obtenida desde la página [Oferta de lugares](https://www.dgae.unam.mx/Licenciatura2025/oferta_lugares/oferta_licenciatura2025.html).

**Las páginas anteriores no son estáticas**, por lo que el contenido podría no estar disponible hasta el próximo concurso de selección.

## Instalación de dependencias

```bash
pip install -r requirements.txt
```

Por otro lado, este proyecto utiliza el navegador Google Chrome y su driver correspondiente, por lo que será necesario que lo descargarlo y adaptar ambos scripts a la ruta correspondiente del driver. Para más información sobre ChromeDriver consulta [aquí](https://developer.chrome.com/docs/chromedriver/downloads).

## En proceso

Se está trabajando en una aplicación web con [shiny](https://shiny.posit.co/) con python para visualizar los datos. 

## Consideraciones legales y éticas

Los datos extraídos por estos scripts provienen de páginas públicas del sitio oficial de la DGAE-UNAM.

Este repositorio no publica ni redistribuye los datos extraídos, y los scripts han sido desarrollados únicamente con fines educativos y de exploración técnica.

Si la institución considera que este repositorio incumple sus políticas, el contenido será retirado o ajustado según se solicite.
