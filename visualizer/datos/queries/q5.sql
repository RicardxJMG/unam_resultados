WITH demanda_carreras AS (
        SELECT 
            id_area,
            id_carrera,
            id_facultad,
            COUNT(*) AS demanda
        FROM resultados_2025 
        GROUP BY id_carrera, id_facultad),
    acreditados_carrera AS (
        SELECT 
        id_area,
        id_carrera,
        id_facultad,
        COUNT(acreditado) as n_resultado
        FROM resultados_2025 
        WHERE acreditado = 'Seleccionado'
        GROUP BY id_carrera, id_facultad, acreditado
     )


SELECT 
    d.id_area,
    c.carrera,
    f.facultad,
    d.demanda, 
    cd.oferta, 
    cd.aciertos_minimos,
    ac.n_resultado AS seleccionados
FROM 
    demanda_carreras d 
JOIN 
    carreras_descripcion cd ON cd.id_carrera = d.id_carrera AND cd.id_facultad = d.id_facultad 
JOIN 
    acreditados_carrera ac ON ac.id_carrera = d.id_carrera AND ac.id_facultad = d.id_facultad
JOIN
    carreras_info c ON c.id_carrera = d.id_carrera  
JOIN 
    facultades_info f ON f.id_facultad = d.id_facultad 
ORDER BY 
    aciertos_minimos DESC

