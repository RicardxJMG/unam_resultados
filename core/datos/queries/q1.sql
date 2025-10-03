--- conteo de aspirantes por area y resultado obtenido

SELECT 
    a.id_area,
    a.area,
    r.acreditado AS resultado,
    COUNT(*) AS n_aspirantes,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje,
    COUNT(CASE WHEN r.puntaje == 120 THEN 1 END) AS puntaje_perfecto   

FROM 
    resultados_2025 r
JOIN 
    areas_info a ON a.id_area = r.id_area
GROUP BY 
    r.id_area, r.acreditado
ORDER BY 
    porcentaje DESC

