import solara
import datos
from vista_mis import ReporteMIS
from vista_registro import Registro

conn = datos.conectar()
periodo = solara.reactive("2026-01")


@solara.component
def Page():
    solara.Title("Recolección de residuos")
    solara.Markdown("# Recolección de residuos")
    solara.Select(label="Periodo", value=periodo, values=["2026-01", "2026-02", "2026-03"])
    ReporteMIS(conn, periodo.value)
    with solara.Card("Registrar una recolección"):
        Registro(conn)
