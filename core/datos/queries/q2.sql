--- calculo de porcentaje por escuela/facultad y estado de acreditado

SELECT 
    r.id_area,  
    f.facultad,
    r.acreditado AS resultado,
    COUNT(*) AS n_aspirantes,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje
FROM 
    resultados_2025 r
JOIN 
    facultades_info f ON f.id_facultad = r.id_facultad
GROUP BY 
    r.id_facultad, r.acreditado
ORDER BY 
    porcentaje DESC
