--- comparación de demanda 2024 vs 2025 de carreras

WITH demanda_2025 AS (
    SELECT 
        r.id_carrera,
        r.id_facultad,
        COUNT(*) AS demanda_2025
    FROM resultados_2025 r
    GROUP BY r.id_carrera, r.id_facultad
)

SELECT
    a.id_area,
    c.carrera,
    f.facultad,
    d25.demanda_2025,
    o24.oferta_2025,
    o24.oferta_2024,
    o24.demanda_2024
FROM demanda_2025 d25
JOIN oferta_2024_2025 o24
    ON d25.id_carrera = o24.id_carrera AND d25.id_facultad = o24.id_facultad
JOIN carreras_info c
    ON d25.id_carrera = c.id_carrera
JOIN facultades_info f
    ON d25.id_facultad = f.id_facultad
JOIN areas_info a 
    ON o24.id_area = a.id_area
