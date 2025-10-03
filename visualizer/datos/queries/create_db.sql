-- PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS areas_info;
DROP TABLE IF EXISTS facultades_info;
DROP TABLE IF EXISTS carreras_info;
DROP TABLE IF EXISTS carreras_descripcion;
DROP TABLE IF EXISTS resultados_2025;
DROP TABLE IF EXISTS oferta_2024_2025;

CREATE TABLE areas_info(
    id_area TEXT PRIMARY KEY,
    area TEXT
);

CREATE TABLE facultades_info(
    id_facultad TEXT PRIMARY KEY,
    facultad TEXT
);

CREATE TABLE carreras_info(
    id_carrera TEXT PRIMARY KEY,
    id_area TEXT,
    carrera TEXT,
    FOREIGN KEY (id_area) REFERENCES areas_info(id_area)
);

CREATE TABLE carreras_descripcion(
    id_carrera TEXT,
    id_area TEXT,
    id_facultad TEXT, 
    oferta INTEGER,
    aciertos_minimos INTEGER,
    FOREIGN KEY (id_carrera) REFERENCES carreras_info(id_carrera),
    FOREIGN KEY (id_area) REFERENCES areas_info(id_area),
    FOREIGN KEY (id_facultad) REFERENCES facultades_info(id_facultad)
);

CREATE TABLE resultados_2025(
    id_aspirante TEXT PRIMARY KEY,
    id_area TEXT,
    id_facultad TEXT,
    id_carrera TEXT,
    puntaje INTEGER,
    acreditado TEXT,
    FOREIGN KEY (id_area) REFERENCES areas_info(id_area),
    FOREIGN KEY (id_facultad) REFERENCES facultades_info(id_facultad),
    FOREIGN KEY (id_carrera) REFERENCES carreras_info(id_carrera)
);

CREATE TABLE oferta_2024_2025(
    id_area TEXT,
    id_carrera TEXT,
    id_facultad TEXT,
    oferta_2025 INTEGER,
    oferta_2024 INTEGER,
    demanda_2024 INTEGER,
    FOREIGN KEY (id_area) REFERENCES areas_info(id_area),
    FOREIGN KEY (id_carrera) REFERENCES carreras_info(id_carrera),
    FOREIGN KEY (id_facultad) REFERENCES facultades_info(id_facultad)
);