--- calculo de porcentaje por carrera y estado de acreditado

SELECT 
    c.id_carrera,
    c.carrera,
    r.acreditado AS resultado,
    COUNT(*) AS n_aspirantes,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje
FROM 
    resultados_2025 r
JOIN 
    carreras_info c ON c.id_carrera = r.id_carrera
GROUP BY 
    r.id_carrera, r.acreditado
ORDER BY 
    porcentaje DESC