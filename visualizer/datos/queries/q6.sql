SELECT 
    r.id_aspirante,
    r.id_area, 
    c.carrera, 
    r.puntaje, 
    cd.aciertos_minimos
FROM resultados_2025 r 
JOIN carreras_info c ON r.id_carrera = c.id_carrera
JOIN carreras_descripcion cd ON r.id_carrera  = cd.id_carrera
WHERE puntaje IS NOT NULL