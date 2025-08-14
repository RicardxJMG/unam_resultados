--- Calculo de porcentaje por area

SELECT 
    a.area,
    COUNT(*) AS total_area,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje
FROM 
    resultados_2025 r
JOIN 
    areas_info a ON a.id_area = r.id_area
GROUP BY 
    a.area
ORDER BY 
    porcentaje DESC

