"""Capa de datos del caso guiado: funciones con ?, sin pantallas."""
import sqlite3
from pathlib import Path

AQUI = Path(__file__).parent  # la carpeta de este archivo; nunca una ruta fija de su equipo


def conectar():
    """Abre base.db. Si no existe (p. ej. en la nube), la crea con esquema.sql y semilla.sql."""
    nueva = not (AQUI / "base.db").exists()
    conn = sqlite3.connect(AQUI / "base.db", check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")  # que SQLite revise las llaves foráneas
    if nueva:
        conn.executescript((AQUI / "esquema.sql").read_text(encoding="utf-8"))
        conn.executescript((AQUI / "semilla.sql").read_text(encoding="utf-8"))
        conn.commit()
    return conn


def consultar(conn, cod_mpio):
    """Consulta (TPS): los registros de un municipio."""
    sql = """SELECT periodo, material, toneladas FROM recolecciones
             WHERE cod_mpio = ? ORDER BY periodo, material"""
    return conn.execute(sql, (cod_mpio,)).fetchall()


def reportar(conn, periodo):
    """Reporte (MIS): toneladas por municipio en un mes."""
    sql = """SELECT m.nombre, ROUND(SUM(r.toneladas), 1) AS total
             FROM recolecciones r JOIN municipios m ON m.cod_mpio = r.cod_mpio
             WHERE r.periodo = ?
             GROUP BY m.nombre ORDER BY total DESC"""
    return conn.execute(sql, (periodo,)).fetchall()


def registrar(conn, cod_mpio, periodo, material, toneladas):
    """Registro (TPS): True si la base acepta la fila; False si la rechaza."""
    sql = """INSERT INTO recolecciones (cod_mpio, periodo, material, toneladas)
             VALUES (?, ?, ?, ?)"""
    try:
        conn.execute(sql, (cod_mpio, periodo, material, toneladas))
        conn.commit()
        return True
    except sqlite3.IntegrityError as error:  # la base rechazó la fila: se avisa, no se esconde
        conn.rollback()
        print("Rechazado por la base:", error)
        return False
