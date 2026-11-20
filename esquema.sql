CREATE TABLE municipios (
    cod_mpio TEXT PRIMARY KEY,
    nombre   TEXT NOT NULL
);
CREATE TABLE recolecciones (
    id        INTEGER PRIMARY KEY,
    cod_mpio  TEXT NOT NULL REFERENCES municipios(cod_mpio),
    periodo   TEXT NOT NULL,
    material  TEXT NOT NULL,
    toneladas REAL NOT NULL CHECK (toneladas > 0)
);
